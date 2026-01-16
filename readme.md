# what are the way to extract information form website to our local system ?
1. Rss feed [use when website is a news / blog / media site  and we need some amount of data]
2. official API [use when you need structured, clean, stable data]
3. web crawling [use when we need lots of data at large scale] some time it is not legal 
4. static web scraping [website where the data is already present in the HTML source returned by the server.]
5. dynamic web scraping [websites where content is loaded via JavaScript after the page loads, requiring browser automation or API interception.]



# we use RSS feed way
some note for rss parsing library (i.e. xml file parser)
1. feedparser-------------easy to use and rss-specific , handle XML file complexity
2. beautifulSoup(xml)-----flexible, when RSS feed is messy and also we use it for HTML file
3. lxml-------------------for big feed

# so we use feedparser libray 
it parse rss_feed and convert them into python object which is look like dictionary.
feed.entries it contain the list of news 
one entry is look like
entry = feed.entries[0]
{
  'title': 'AI beats humans at coding',
  'link': 'https://www.bbc.co.uk/news/technology-123456',
  'summary': '<p>AI systems are now...</p>',
  'published': 'Thu, 16 Jan 2026 08:00:00 GMT',
  'published_parsed': time.struct_time(
        tm_year=2026, tm_mon=1, tm_mday=16,
        tm_hour=8, tm_min=0, tm_sec=0
  )
}

#rss_feed link of BBC
https://feeds.bbci.co.uk/news/technology/rss.xml



# task
 in this task i write an code , where user can provide multiple rss_fee_link of bcc as input and my code extract few info from that xml file and save then into excel file as output.
 title / description/ time/ link/category/source 



# this task is I/O-bound means the program spends most of its time waiting, not computing. example Network requests (HTTP, API calls) /Disk read or write /Database queries
# cpu-bound means cooking yourself and i/o- bound means ordering food. 

# if user give the large number of input link then we have to apply parallelism in our code for that their are different-2 ways.
1. asyncio with aiohttp (if we working on I/O- bound used this )
2. ThreadPoolExecutor (if we have small code not for very critical or heavy task then we use this way)
3. multiprocessing (if CPU- bound)
4. ProcessPoolExecutor (if CPU-bound and it is high-level of multiprocessing)
5. apache spark(distributed computing) - for big data not for rss feed

# in our case may be we can use asyncio 
# why?
 in threadPollexecutor , it create multiple oOS thread (unit excecution), each thread run independently, Each thread blocks(means the thread stops executing until an operation finishes.) while waiting for HTTP response
 Async is deal with waiting problem, not for computational speed. it downloads RSS data from the internet, but does not stop the rest of the program from running while it waits for the network response.

# example :
 1 worker deal with 1 tables ,kitchen say wait 10 min then waiter is waiting not do any thing. so similarly if we have 10 waiter
 where as in async we have only one waiter who deal with all the tables in the restraun , if kitchen say with 10 min for table 1 it go to table 2.   

# Why threadpoolexcecutor is inefficient?
# Problems
#Threads consume RAM (Each thread gets Its own stack used for:[Function calls/Local variables/Return addresses] Even if the thread is waiting, stack memory is still reserved.
#Too many threads → context switching overhead
#Most threads are idle
#Doesn’t scale well for 1000s of requests

# async reduce walk-time not time complexity 
# time complexity of my code od O(N**2)