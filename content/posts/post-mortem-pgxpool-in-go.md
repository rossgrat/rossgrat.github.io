{
   "date": "2024-04-20T18:55:54-04:00",
   "draft": true,
   "title": "pgxpool Hangs in Go Database Transactions - Post-Mortem",
   "tags" : [
      "post-mortem",
      "go",
      "database"
   ]
}

Things move pretty fast in a startup. So fast that sometimes there isn't time to stop and reflect on the solution to a difficult problem. But I am of the opinion that it is best to write down and record mistakes in order to prevent that same mistake from occuring in the future. I think mistakes are valuable learning experiences that should be processed and absorbed into my everyday work routines so that if the same issue appears again someday, I am ready for it.

I encountered quite the mysterious bug at work around a month ago that caused our production server to completely stop responding to and logging requests, seemingly at random. This bug would completely lock up our server until an engineer manually restarted it.

First step: Pre-logging HTTP request
Second step: Braingstorming

Fix: deferring the closing of rows in pgxpool 

Lets dive in and take a look at why this occured, the underlying mechanics of the problem, and how it can be resolved.