from agent_core import ProductionAgent

TEST_CASES = [
    {"id":1,"query":"成都AI Agent开发薪资","diff":"简单","expect":["成都","23K","38K"]},
    {"id":2,"query":"我适合什么工作","diff":"中等","expect":["AI Agent","Python"]},
    {"id":3,"query":"做职业规划","diff":"困难","expect":["职业规划","技能","岗位"]},
]

def run_eval():
    agent = ProductionAgent()
    user = {"city":"成都","target_job":"AI Agent应用开发"}
    passed = 0
    for case in TEST_CASES:
        ans,_ = agent.run(case["query"], user)
        ok = all(k in ans for k in case["expect"])
        if ok: passed +=1
        print(f"用例 {case['id']} → {'✅ 通过' if ok else '❌ 失败'}")
    print(f"\n通过率：{passed}/{len(TEST_CASES)} = {passed/len(TEST_CASES)*100:.1f}%")

if __name__ == "__main__":
    run_eval()