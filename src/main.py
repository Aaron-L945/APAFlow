from langgraph.graph import StateGraph, END 
from graph.state import AgentState, l1_dom_node, l2_vision_node, l3_human_node
from core.browser import Browser # Import Browser class

# Placeholder for undefined functions, will need user input for actual implementation
def should_fallback_to_vision(state: AgentState):
    # Implement logic to decide if fallback to vision node is needed
    # If l1_dom_node failed (indicated by last_error), fallback to vision
    if state["last_error"]:
        return "fail"
    return "success"

def should_fallback_to_human(state: AgentState):
    # Implement logic to decide if fallback to human node is needed
    # If l2_vision_node failed (indicated by last_error), fallback to human
    if state["last_error"]:
        return "fail"
    return "success"

workflow = StateGraph(AgentState) 

# 1. 添加节点 
workflow.add_node("l1_dom", l1_dom_node) 
workflow.add_node("l2_vision", l2_vision_node) 
workflow.add_node("l3_human", l3_human_node) 

# 2. 设置连线逻辑 
workflow.set_entry_point("l1_dom") 

# 核心路由：L1 报错走 L2，L2 报错走 L3 
workflow.add_conditional_edges( 
    "l1_dom", 
    should_fallback_to_vision, # 自定义逻辑函数 
    {"success": END, "fail": "l2_vision"} 
) 
workflow.add_conditional_edges( 
    "l2_vision", 
    should_fallback_to_human, 
    {"success": END, "fail": "l3_human"} 
) 
workflow.add_edge("l3_human", END) 

app = workflow.compile()

async def main():
    browser_instance = Browser()
    # await browser_instance.start() # Start the browser once

    # Example usage:
    initial_state = AgentState(
        goal="Perform a task on a webpage",
        url="about:blank",
        dom_snippet="",
        screenshot=None,
        last_error="",
        retry_count=0,
        results=[],
        browser=browser_instance # Pass the browser instance
    )
    
    # Run the workflow
    # For a real application, you would pass a real state and handle the output
    # For now, we just demonstrate the setup
    print("Workflow compiled. Ready to run.")
    # result = await app.ainvoke(initial_state) # Uncomment to run the workflow
    # print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())