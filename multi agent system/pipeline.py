from agents import build_search_agent , build_reader_agent , writer_chain , critic_chain

def run_research_pipeline (topic:str) -> dict :

    state={}

#search_agent invoking

    print("\n" + "="*50)
    print("STEP 1 - Search Agent Is Working")
    print("="*50)

    search_agent = build_search_agent ()
    search_result = search_agent.invoke ({  
        "messages" : [("user", f"Find recent and reliable information about given : {topic}")]
    }) 
    state["search_results"] = search_result['messages'][-1].content
    print("\n search result  :"   , state["search_results"])

#reader_agent invoking

    print("\n" + " ="*50)
    print("STEP 2 - Reader Agent is scraping the URLs")
    print("="*50)
    reader_agent = build_reader_agent ()
    reader_result =reader_agent.invoke ({
        "messages" : [( "user",
            f"Based on the following search results about '{topic}',"
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results' ] [: 2000] }"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n scraped content :" ,  state['scraped_content'])

#writer chain

    print("\n" + " ="*50)
    print("STEP 3 - Writer is drafting the report...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n{state['search_results']} \n\n"
        f"DETAILED SCREPEED CONTENT    : \n{state['scraped_content']}"
    )
    
    state["report"] = writer_chain.invoke ({
          "topic": topic,
         "research": research_combined
    })

    print("\n Final Report :", state['report'] )

#critic chain 

    print("\n" + " ="*50)
    print("STEP 4 - Critic is revviewing the report...")
    print("="*50)

    state["feedback"] = critic_chain.invoke ({
        "report" : state["report"]

    }
    )
    print("\n critic report :", state['feedback'])
   
    return state

if __name__ == "__main__" :
    topic = input("\n Enter Research Topic : ")
    run_research_pipeline(topic)
    


