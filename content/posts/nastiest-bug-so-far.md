{
   "date": "2025-01-20T16:29:40-05:00",
   "draft": false,
   "title": "The Nastiest Bug I Have Fixed (So Far)",
   "tags" : [
      "technical",
      "go",
      "database",
      "backend"
   ]
}

## Edit - October 9th, 2025

It's a bit embarassing to look back at this post (even though it was originally posted less than a year ago!) and realize that the "fixed" code isn't quite fixed. After many months of learning from talented engineers in my new position, and finishing Kleppmann's Designing Data-Intensive Applications (a.k.a the Bible), I realize that there is actually a read skew condition present in the "fixed" code. The correct fix for this bug is to use transactions and leverage Snapshot Isolation present in Postgres.

Live and learn!

## Original Post

As I enter my last week at my current company, I thought it might be fun to do a quick writeup on the bug that was the hardest for me to track down and fix in the last two and a half years. 

In the early spring of 2024, I encountered quite the mysterious bug that caused our production monolith server to completely stop responding to and logging requests, seemingly at random. This bug would lock up our server until an engineer manually restarted it. While the investigation process was an ordeal on its own, the main thing I want to focus on in this article is the bug itself.

Before I explain the bug, I am going to lay it out so you can have a guess. I have recreated the bug in an abbreviated version of the culprit code below. I have omitted the SQL statements, error checking, and database connection pool initialization. All you need to know, besides the code below, is that the Postgres database connection pool is initialized via the `jackc/pgxpool/v4` package and is shared globally among all of the concurrent server threads. Queries are made via the `jackc/pgx` package.

{{< highlight golang >}}
rows, _ := ConnPool.Query()
for rows.Next(){
   // Scan and process row
   newRows, _ := ConnPool.Query()
   for newRows.next() {
      // Scan and process new row
   }
}
{{< /highlight >}}

Do you see the problem? Maybe? What if I rewrite it with mutexes?

{{< highlight golang >}}
mutex.Lock()
for i := 0; i < 1000; i++ {
   mutex.Lock()
   for j := 0; j < 10; j++ {
      // Do stuff
   }
   mutex.Unlock()
}
mutex.Unlock()
{{< /highlight >}}

This is indeed a deadlock caused by a sneaky race condition.

Upon creation, each database pool accepts a config object that defines important things, but the particularly relevant field for my case was the maximum number of connections field (`MaxConns`). The definition of this from the `pgxpool` package is below.
{{< highlight golang >}}
	// MaxConns is the maximum size of the pool. The default is the greater of 4 or runtime.NumCPU().
	MaxConns int32
{{< /highlight >}}

The production monolith has only four CPU cores, so the maximum number of database connections is 4.

A database connection is taken from the pool when `ConnPool.Query()` is called, but the connection is not released back into the pool until either one of two things (to my knowledge) occurs:
1. `rows.Close()` is called on the open `rows` object.
2. `rows.Next()` completes iterating over all available rows.

You can see in the example that there are two `ConnPool.Query()` calls, with one nested under the other. The first `rows` object does not release its connection back into the pool until after the function acquires a second connection from the pool and fully processes it.

In the overall context of this bug in our server; on quick, subsequent calls to the endpoint that invoked this database code, four separate threads would each take a database connection before any of them could grab a second connection. This would effectively lock up the database layer, because each of these threads is now waiting for a second database connection, while holding onto their own initial connection.

This fix was a simple one.
{{< highlight golang >}}
rows, _ := ConnPool.Query()
var data []any
for rows.Next(){
   // Scan and process rows into data
}

newRows, _ := ConnPool.Query()
for newRows.next() {
   // Scan and process new rows using data
}
{{< /highlight >}}

Thanks for reading! I've also attached some additional links on database connection pools if you want to read a little more about why they are used.
- [StackOverflow](https://stackoverflow.com/questions/4041114/what-is-database-pooling)
- [Cochroack Labs](https://www.cockroachlabs.com/blog/what-is-connection-pooling/)