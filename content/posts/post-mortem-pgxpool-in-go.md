{
   "date": "2024-12-10T18:22:00-04:00",
   "draft": true,
   "title": "HTTP Server Deadlocks from Database Connection Exhaustion",
   "tags" : [
      "post-mortem",
      "go",
      "database",
      "postgres"
   ]
}

Things move pretty fast in a startup. So fast that sometimes there isn't time to stop and reflect on the solution to a difficult problem. But I am of the opinion that it is best to write down and record mistakes in order to prevent that same mistake from occuring in the future. I think mistakes are valuable learning experiences that should be processed and absorbed into my everyday work routines so that if the same issue appears again someday, I am ready for it.

I encountered quite the mysterious bug that caused our production server to completely stop responding to and logging requests, seemingly at random. This bug would completely lock up our server (foreshadowing) until an engineer manually restarted it. In the sections below, I want to discuss what I did to locate this bug, why it occured, and how I fixed it.

Links to read:
https://azure.microsoft.com/en-us/blog/summary-of-windows-azure-service-disruption-on-feb-29th-2012/
https://pkg.go.dev/github.com/jackc/pgx/v4/pgxpool#Config
https://stackoverflow.com/questions/4041114/what-is-database-pooling
https://www.cockroachlabs.com/blog/what-is-connection-pooling/

## 

First step: Pre-logging HTTP request
Second step: Braingstorming

Fix: deferring the closing of rows in pgxpool 

Lets dive in and take a look at why this occured, the underlying mechanics of the problem, and how it can be resolved.
