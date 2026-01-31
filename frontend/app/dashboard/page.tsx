'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

interface StudentLog {
  timestamp: string;
  course_id: string;
  action: string;
  decision: string;
  actor_id_pseudonym: string;
}

export default function Dashboard() {
  const [logs, setLogs] = useState<StudentLog[]>([]);
  const [pseudonym, setPseudonym] = useState('student_001');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [liveCount, setLiveCount] = useState(3);

  // Simulate live event updates
  useEffect(() => {
    if (logs.length > 0) {
      const interval = setInterval(() => {
        setLiveCount((prev) => prev + 1);
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [logs]);

  const fetchLogs = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(
        `http://localhost:8000/api/transparency/my-logs/${pseudonym}`
      );
      if (!res.ok) throw new Error('Failed to fetch logs');
      const data = await res.json();
      setLogs(data.logs || []);
      setLiveCount((data.logs || []).length || 3);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    }
    setLoading(false);
  };

  const timeline = logs.length
    ? logs.map((log) => ({
        title: `${new Date(log.timestamp).toLocaleDateString()}: ${log.action}`,
        subtitle: `${log.course_id} — ${log.decision}`,
      }))
    : [
        { title: 'Jan 29: Brainstorm', subtitle: 'CS101 — ALLOW' },
        { title: 'Jan 28: Code Review', subtitle: 'CS101 — ALLOW' },
        { title: 'Jan 26: Full Solution', subtitle: 'CS101 — DENY' },
      ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-teal-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-8 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-indigo-600">
            EVGG
          </Link>
          <div className="flex gap-4">
            <Link href="/" className="text-gray-600 hover:text-gray-800">
              Home
            </Link>
            <Link href="/copilot" className="text-indigo-600 font-semibold">
              Copilot
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Student Dashboard</h1>
          <p className="text-gray-600">Privacy‑safe AI usage log (metadata only)</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-10">
          <Card className="hover:shadow-lg transition-shadow animate-in fade-in duration-500">
            <CardHeader>
              <CardTitle>Your AI Record</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold text-gray-900 mt-2 animate-pulse">
                {liveCount} events ✅
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Logs are anonymized and visible only to you.
              </p>
            </CardContent>
          </Card>
          <Card className="hover:shadow-lg transition-shadow animate-in fade-in duration-500 delay-100">
            <CardHeader>
              <CardTitle>Active Course</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold text-gray-900 mt-2">CS101</p>
              <p className="text-sm text-gray-500 mt-2">
                Governance decisions with real‑time policy checks.
              </p>
            </CardContent>
          </Card>
          <Card className="hover:shadow-lg transition-shadow animate-in fade-in duration-500 delay-200">
            <CardHeader>
              <CardTitle>Privacy Legend</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="text-sm text-gray-700 space-y-2">
                <li>• No PII stored</li>
                <li>• Metadata only</li>
                <li>• Auto‑delete after 90 days</li>
              </ul>
            </CardContent>
          </Card>
        </div>

        <Card className="mb-8">
          <CardContent className="pt-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Enter your pseudonym
          </label>
          <div className="flex flex-wrap gap-3">
            <Input
              value={pseudonym}
              onChange={(e) => setPseudonym(e.target.value)}
              placeholder="e.g., student_001"
              className="flex-1 min-w-[220px]"
            />
            <Button onClick={fetchLogs} disabled={loading} className="hover:scale-105 transition-transform">
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Loading...
                </span>
              ) : (
                'View Logs'
              )}
            </Button>
          </div>
          </CardContent>
        </Card>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            Error: {error}
          </div>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Timeline</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {timeline.map((event, idx) => (
              <div key={idx} className="flex items-start gap-3 animate-in fade-in slide-in-from-left duration-500" style={{ animationDelay: `${idx * 100}ms` }}>
                <span className="mt-2 h-2 w-2 rounded-full bg-emerald-500 animate-pulse" aria-hidden="true" />
                <div>
                  <p className="text-sm font-semibold text-gray-900">{event.title}</p>
                  <p className="text-xs text-gray-500">{event.subtitle}</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
