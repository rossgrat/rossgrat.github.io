{
   "date": "2025-01-20T16:29:40-05:00",
   "draft": true,
   "title": "The Nastiest Bug I Have Fixed (So Far)",
   "tags" : [
      "technical",
      "go",
      "database",
      "backend",
      "concurrency"
   ]
}

As I enter my last week at my current company, I thought it might be fun to do a writeup on the bug that was the hardest for me to track down and fix in the last two and a half years. 

In the early spring of 2024, I encountered quite the mysterious bug that caused our production monolith server to completely stop responding to and logging requests, seemingly at random. This bug would lock up our server until an engineer manually restarted it. While the investigation process was an ordeal on its own, the main thing I want to focus on in this article is the bug itself, so I will be omitting the gory details of how I tracked down and squashed this bug.

The problem ended up being a bug in the allocation and management of database connections from a shared database connection pool.

## Background
I'll start with some background

A database connection pool is a group of database connections that are initialized in

The package used was jackc's pgxpool for Go

Each database pool accepts a config object that defines important things, such as callback functions run before and after acquiring a connection, the maximum lifetime of a given database connection, and the maximum time that a connection can be idle, to name a few. A particularly relevant field for my case was the maximum number of connections field (`MaxConns`). The definition of this from the `pgxpool` package is below.
{{< highlight golang >}}
	// MaxConns is the maximum size of the pool. The default is the greater of 4 or runtime.NumCPU().
	MaxConns int32
{{< / highlight >}}

The production monolith has only four CPU cores, so the maximum number of CPU cores is 4.

## The Bug
I have reproduced the bug below in a an abbreviated version of the culprit code. For simplicity and clarity I have omitted error checking, as well as the setup function initializing the connection pool. You can assume that all error checking is done correctly and that the connection pool is initialized correctly.

{{< highlight golang >}}
var ConnPool *pgxpool.Pool

func GetPersonsInGroup(groupID int)[]Person{

   for rows.Next(){


   }
}
{{< / highlight >}}

Do you see the problem? Maybe? What if I rewrite it with mutexes?

{{< highlight golang >}}
{{< / highlight >}}

Here's the fix.
{{< highlight golang >}}
{{< / highlight >}}

Links to read:
https://pkg.go.dev/github.com/jackc/pgx/v4/pgxpool#Config
https://stackoverflow.com/questions/4041114/what-is-database-pooling
https://www.cockroachlabs.com/blog/what-is-connection-pooling/