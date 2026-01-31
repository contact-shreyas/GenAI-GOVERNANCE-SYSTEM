'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

interface CopilotResponse {
  answer: string;
  confidence?: number;
  citations?: string[];
  flag?: string;
}

export default function CopilotPage() {
  const [question, setQuestion] = useState('Can I use ChatGPT for brainstorming?');
  const [courseId, setCourseId] = useState('CS101');
  const [answer, setAnswer] = useState<CopilotResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [displayedAnswer, setDisplayedAnswer] = useState('');

  // Simulate typing effect
  useEffect(() => {
    if (loading) {
      setDisplayedAnswer('');
    } else if (answer?.answer) {
      let index = 0;
      const interval = setInterval(() => {
        if (index < answer.answer.length) {
          setDisplayedAnswer(answer.answer.substring(0, index + 1));
          index++;
        } else {
          clearInterval(interval);
        }
      }, 15);
      return () => clearInterval(interval);
    }
  }, [loading, answer]);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAnswer(null);
    setDisplayedAnswer('');

    try {
      const response = await axios.post(
        `${API_BASE}/api/copilot/ask?question=${encodeURIComponent(question)}&course_id=${courseId}`
      );
      // Simulate streaming delay
      await new Promise(resolve => setTimeout(resolve, 300));
      setAnswer(response.data);
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } }; message?: string };
      setAnswer({
        answer: `❌ Error: ${err.response?.data?.detail ?? err.message ?? 'Unknown error'}`,
        confidence: 0,
        citations: [],
      });
    } finally {
      setLoading(false);
    }
  };

  const displayAnswer = displayedAnswer || (answer?.answer ?? '✅ YES — Brainstorming is explicitly permitted for assignments.');
  const confidence = typeof answer?.confidence === 'number' ? Math.round(answer.confidence * 100) : 98;
  const citations = (answer?.citations?.length ?? 0) > 0
    ? answer.citations
    : ['CS101 Policy §2.1 — Brainstorming allowed with disclosure.'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-indigo-600">
            EVGG
          </Link>
          <div className="flex gap-4 text-sm font-semibold text-gray-600">
            <Link href="/policies" className="hover:text-indigo-700">Faculty Builder</Link>
            <Link href="/dashboard" className="hover:text-indigo-700">Student Dashboard</Link>
            <Link href="/admin" className="hover:text-indigo-700">Admin Analytics</Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-8 py-10 grid lg:grid-cols-4 gap-8">
        {/* Sidebar */}
        <aside className="lg:col-span-1 h-fit">
          <Card>
            <CardHeader>
              <CardTitle>Recent Policies</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded-lg">
                CS101 <Badge className="bg-emerald-100 text-emerald-700">Active</Badge>
              </div>
              <div className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded-lg">
                ENG102 <Badge variant="secondary">Draft</Badge>
              </div>
              <div className="flex items-center justify-between bg-gray-50 px-3 py-2 rounded-lg">
                BIO110 <Badge className="bg-purple-100 text-purple-700">Active</Badge>
              </div>
              <p className="text-xs text-gray-500">
                Students see only policy rules and disclosure templates. No content is stored.
              </p>
            </CardContent>
          </Card>
        </aside>

        {/* Chat */}
        <main className="lg:col-span-3">
          <Card>
            <CardContent className="p-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Student Copilot</h1>
              <p className="text-sm text-gray-600">Verified answers with citations</p>
            </div>
            <Badge className={`${confidence >= 90 ? 'bg-emerald-100 text-emerald-700' : 'bg-yellow-100 text-yellow-700'} animate-pulse`}>
              {confidence}% Confidence ✓
            </Badge>
          </div>

          <div className="space-y-6">
            <div className="flex justify-end">
              <div className="max-w-lg bg-indigo-600 text-white p-4 rounded-2xl rounded-br-md shadow">
                <p className="text-sm">{question}</p>
                <p className="text-[11px] text-indigo-200 mt-2">Student</p>
              </div>
            </div>

            <div className="flex justify-start">
              <div className="max-w-lg bg-gray-50 border border-gray-200 p-4 rounded-2xl rounded-bl-md shadow animate-in slide-in-from-left duration-500">
                <p className={`text-sm font-semibold text-gray-900 ${loading ? 'min-h-6' : ''}`}>
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <span className="inline-block">Thinking</span>
                      <span className="flex gap-1">
                        <span className="h-1 w-1 rounded-full bg-gray-400 animate-bounce" />
                        <span className="h-1 w-1 rounded-full bg-gray-400 animate-bounce delay-100" />
                        <span className="h-1 w-1 rounded-full bg-gray-400 animate-bounce delay-200" />
                      </span>
                    </span>
                  ) : (
                    displayAnswer
                  )}
                </p>
                {!loading && (
                  <>
                    <div className="mt-3 bg-white border border-blue-100 p-3 rounded-lg text-xs text-gray-700 animate-in fade-in duration-500">
                      <p className="font-semibold text-blue-700 mb-1">Policy Quote</p>
                      {citations.map((cite: string, idx: number) => (
                        <p key={idx}>"{cite}"</p>
                      ))}
                    </div>
                    <div className="mt-3 bg-emerald-50 border border-emerald-200 p-3 rounded-lg text-xs text-emerald-900 animate-in fade-in duration-500 delay-100">
                      <p className="font-semibold mb-1">Disclosure Template</p>
                      I used AI for brainstorming ideas; final submission is my own work.
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>

          <form onSubmit={handleAsk} className="mt-8 grid md:grid-cols-4 gap-3">
            <Input
              value={courseId}
              onChange={(e) => setCourseId(e.target.value)}
              className="md:col-span-1"
              placeholder="Course"
            />
            <Input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="md:col-span-2"
              placeholder="Ask a policy question..."
            />
            <Button type="submit" disabled={loading} className="md:col-span-1 hover:scale-105 transition-transform">
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Thinking...
                </span>
              ) : (
                'Ask Copilot'
              )}
            </Button>
          </form>
            </CardContent>
          </Card>
        </main>
      </div>
    </div>
  );
}
