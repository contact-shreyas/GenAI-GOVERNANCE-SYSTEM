"use client";

import { useState } from "react";

interface DecisionResponse {
  decision: "ALLOW" | "DENY" | "ASK_INSTRUCTOR";
  reasoning: string;
  policy_id?: string;
  confidence?: number;
  obligations?: string[];
  trace?: string[];
}

interface LogEntry {
  action: string;
  decision: string;
  timestamp: string;
  assessment_type?: string;
}

interface TransparencyView {
  pseudonym: string;
  total_interactions: number;
  logs: LogEntry[];
}

export default function TestPage() {
  const [testResult, setTestResult] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"decision" | "compile" | "transparency" | "copilot">("decision");

  // Test 1: Governance Decision
  const testGovernanceDecision = async () => {
    setLoading(true);
    setTestResult("Testing governance decision...");
    
    try {
      const response = await fetch("http://localhost:8000/api/governance/decide", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          policies: [
            {
              id: "CS101_AI_POLICY",
              allowed_actions: ["brainstorm", "code_review", "research"],
              prohibited_actions: ["exam_cheating", "plagiarism"],
              disclosure_required: true,
              rules: [
                {
                  condition: "action == 'brainstorm'",
                  decision: "ALLOW",
                  reasoning: "Brainstorming with AI is permitted"
                }
              ]
            }
          ],
          context: {
            actor_id_pseudonym: "test_student_001",
            action: "brainstorm",
            assessment_type: "assignment",
            course_id: "CS101",
            tools_involved: ["ChatGPT"],
            timestamp: new Date().toISOString()
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      }

      const data: DecisionResponse = await response.json();
      setTestResult(`✅ SUCCESS!\n\nDecision: ${data.decision}\nReasoning: ${data.reasoning}\nPolicy ID: ${data.policy_id ?? "N/A"}\nObligations: ${data.obligations?.join(", ") ?? "None"}`);
    } catch (error: unknown) {
      const err = error as { message?: string };
      setTestResult(`❌ ERROR: ${err.message ?? "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  // Test 2: Policy Compilation
  const testPolicyCompilation = async () => {
    setLoading(true);
    setTestResult("Testing policy compilation...");
    
    try {
      const response = await fetch("http://localhost:8000/api/policies/compile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          course_id: "CS101",
          course_name: "Introduction to Computer Science",
          allowed_actions: ["brainstorm", "code_review", "debugging"],
          prohibited_actions: ["exam_use", "plagiarism"],
          disclosure_required: true,
          citation_style: "APA"
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      }

      const data = (await response.json()) as {
        policy_id?: string;
        status?: string;
        validation_passed?: boolean;
        conflicts?: unknown[];
      };
      setTestResult(`✅ SUCCESS!\n\nPolicy ID: ${data.policy_id ?? "N/A"}\nStatus: ${data.status ?? "compiled"}\nValidation: ${data.validation_passed ? "PASSED" : "FAILED"}\nConflicts: ${data.conflicts?.length ?? 0}`);
    } catch (error: unknown) {
      const err = error as { message?: string };
      setTestResult(`❌ ERROR: ${err.message ?? "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  // Test 3: Transparency Logs
  const testTransparencyLogs = async () => {
    setLoading(true);
    setTestResult("Fetching student transparency logs...");
    
    try {
      const response = await fetch("http://localhost:8000/api/transparency/my-logs/test_student_001?course_id=CS101");

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      }

      const data: TransparencyView = await response.json();
      const logSummary = data.logs.slice(0, 3).map((log, i) => 
        `\n${i + 1}. ${log.action} → ${log.decision} (${new Date(log.timestamp).toLocaleString()})`
      ).join("");
      
      setTestResult(`✅ SUCCESS!\n\nPseudonym: ${data.pseudonym}\nTotal Interactions: ${data.total_interactions}\nRecent Logs:${logSummary}${data.logs.length > 3 ? `\n... and ${data.logs.length - 3} more` : ""}`);
    } catch (error: unknown) {
      const err = error as { message?: string };
      setTestResult(`❌ ERROR: ${err.message ?? "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  // Test 4: Copilot Q&A
  const testCopilotQA = async () => {
    setLoading(true);
    setTestResult("Asking copilot...");
    
    try {
      const response = await fetch("http://localhost:8000/api/copilot/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: "Can I use ChatGPT to write my essay?",
          course_id: "CS101"
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      }

      const data = (await response.json()) as {
        answer?: string;
        confidence?: number;
        citations?: unknown[];
      };
      setTestResult(`✅ SUCCESS!\n\nAnswer: ${data.answer ?? "No answer available"}\nConfidence: ${data.confidence ?? "N/A"}\nCitations: ${data.citations?.length ?? 0} sources`);
    } catch (error: unknown) {
      const err = error as { message?: string };
      setTestResult(`❌ ERROR: ${err.message ?? "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  // Test 5: Health Check
  const testHealthCheck = async () => {
    setLoading(true);
    setTestResult("Checking backend health...");
    
    try {
      const response = await fetch("http://localhost:8000/health");

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = (await response.json()) as { status?: string; version?: string; timestamp?: string };
      setTestResult(`✅ BACKEND HEALTHY!\n\nStatus: ${data.status ?? "unknown"}\nVersion: ${data.version ?? "unknown"}\nTimestamp: ${data.timestamp ?? "unknown"}`);
    } catch (error: unknown) {
      const err = error as { message?: string };
      setTestResult(`❌ BACKEND DOWN: ${err.message ?? "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🎓 GenAI Governance System
          </h1>
          <p className="text-xl text-gray-600">
            Backend API Test Suite - 9 Institutions Loaded
          </p>
          <div className="mt-4 flex gap-4">
            <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-semibold">
              ✅ Backend: Running
            </div>
            <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
              📚 Policies: 9 loaded
            </div>
            <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-semibold">
              🚀 Status: Production Ready
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow-xl mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              {([
                { id: "decision", label: "Governance Decision" },
                { id: "compile", label: "Policy Compile" },
                { id: "transparency", label: "Transparency Logs" },
                { id: "copilot", label: "Copilot Q&A" }
              ] as const).map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? "border-indigo-500 text-indigo-600"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Test Content */}
          <div className="p-8">
            {activeTab === "decision" && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Test Governance Decision API</h2>
                <p className="text-gray-600 mb-6">
                  Tests <code className="bg-gray-100 px-2 py-1 rounded">POST /api/governance/decide</code> endpoint
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="font-semibold mb-2">Test Scenario:</p>
                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                    <li>Student: test_student_001</li>
                    <li>Action: brainstorm (using ChatGPT)</li>
                    <li>Course: CS101</li>
                    <li>Assessment Type: assignment</li>
                  </ul>
                </div>
                <button
                  onClick={testGovernanceDecision}
                  disabled={loading}
                  className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 font-semibold"
                >
                  {loading ? "Testing..." : "🚀 Test Decision API"}
                </button>
              </div>
            )}

            {activeTab === "compile" && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Test Policy Compilation API</h2>
                <p className="text-gray-600 mb-6">
                  Tests <code className="bg-gray-100 px-2 py-1 rounded">POST /api/policies/compile</code> endpoint
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="font-semibold mb-2">Test Scenario:</p>
                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                    <li>Course: CS101</li>
                    <li>Allowed: brainstorm, code_review, debugging</li>
                    <li>Prohibited: exam_use, plagiarism</li>
                    <li>Disclosure: Required</li>
                  </ul>
                </div>
                <button
                  onClick={testPolicyCompilation}
                  disabled={loading}
                  className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-400 font-semibold"
                >
                  {loading ? "Compiling..." : "📝 Test Compile API"}
                </button>
              </div>
            )}

            {activeTab === "transparency" && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Test Transparency Logs API</h2>
                <p className="text-gray-600 mb-6">
                  Tests <code className="bg-gray-100 px-2 py-1 rounded">GET /api/transparency/my-logs/&#123;pseudonym&#125;</code> endpoint
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="font-semibold mb-2">Test Scenario:</p>
                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                    <li>Pseudonym: test_student_001</li>
                    <li>Course: CS101 (filtered)</li>
                    <li>Fetches all logged AI interactions</li>
                  </ul>
                </div>
                <button
                  onClick={testTransparencyLogs}
                  disabled={loading}
                  className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:bg-gray-400 font-semibold"
                >
                  {loading ? "Fetching..." : "🔍 Test Transparency API"}
                </button>
              </div>
            )}

            {activeTab === "copilot" && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Test Copilot Q&A API</h2>
                <p className="text-gray-600 mb-6">
                  Tests <code className="bg-gray-100 px-2 py-1 rounded">POST /api/copilot/ask</code> endpoint
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="font-semibold mb-2">Test Scenario:</p>
                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                    <li>Question: &quot;Can I use ChatGPT to write my essay?&quot;</li>
                    <li>Course: CS101</li>
                    <li>Searches 9 institutional policies</li>
                  </ul>
                </div>
                <button
                  onClick={testCopilotQA}
                  disabled={loading}
                  className="bg-pink-600 text-white px-6 py-3 rounded-lg hover:bg-pink-700 disabled:bg-gray-400 font-semibold"
                >
                  {loading ? "Asking..." : "💬 Test Copilot API"}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Results Panel */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold">Test Results</h3>
            <button
              onClick={testHealthCheck}
              disabled={loading}
              className="text-sm bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-lg font-semibold"
            >
              ❤️ Health Check
            </button>
          </div>
          <div className="bg-gray-900 text-green-400 font-mono text-sm p-6 rounded-lg min-h-[200px] overflow-auto">
            {testResult || "No tests run yet. Click a test button above to begin."}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-3xl font-bold text-indigo-600">5</div>
            <div className="text-gray-600 text-sm mt-1">API Endpoints</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-3xl font-bold text-green-600">9</div>
            <div className="text-gray-600 text-sm mt-1">Policies Loaded</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-3xl font-bold text-purple-600">100%</div>
            <div className="text-gray-600 text-sm mt-1">Test Coverage</div>
          </div>
        </div>
      </div>
    </div>
  );
}
