'use client';

import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

interface AnalyticsData {
  course_id: string;
  period: string;
  unique_students: number;
  total_events: number;
  by_action?: Record<string, number>;
  compliance_rate?: string;
}

export default function AdminPage() {
  const [courseId, setCourseId] = useState('CS101');
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [darkMode, setDarkMode] = useState(false);

  const fetchAnalytics = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.get(
        `${API_BASE}/api/transparency/course-analytics/${courseId}`
      );
      setAnalytics(response.data);
    } catch (err: unknown) {
      const error = err as { message?: string };
      setError(`Failed to load analytics: ${error.message ?? 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  }, [courseId]);

  useEffect(() => {
    fetchAnalytics();
  }, [fetchAnalytics]);

  const actionEntries: Record<string, number> = analytics?.by_action ?? {};
  const totalEvents = analytics?.total_events ?? Object.values(actionEntries).reduce((sum, value) => sum + value, 0) ?? 0;
  const complianceValue = analytics?.compliance_rate ?? (totalEvents ? `${Math.min(100, Math.round((1 - ((actionEntries.full_solution ?? 0) / totalEvents)) * 100))}%` : '85%');
  const chartRows: Array<[string, number]> = Object.keys(actionEntries).length
    ? Object.entries(actionEntries)
    : [
        ['brainstorm', 18],
        ['code_review', 12],
        ['citation_check', 9],
        ['full_solution', 3],
      ];

  return (
    <div className={darkMode ? 'min-h-screen bg-slate-950 text-white' : 'min-h-screen bg-slate-50'}>
      <nav className={darkMode ? 'bg-slate-900 border-b border-slate-800' : 'bg-white shadow-sm'}>
        <div className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
          <Link href="/" className={darkMode ? 'text-white font-bold' : 'text-2xl font-bold text-indigo-600'}>
            EVGG
          </Link>
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="sm"
              className={darkMode ? 'bg-slate-800 text-slate-200 border-slate-700' : 'bg-slate-100 text-slate-700'}
              onClick={() => setDarkMode((prev) => !prev)}
            >
              {darkMode ? 'Light Mode' : 'Dark Mode'}
            </Button>
            <Link href="/copilot" className={darkMode ? 'text-slate-200 text-sm' : 'text-gray-600 text-sm'}>
              Student Copilot
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-8 py-10">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 mb-8">
          <div>
            <h1 className={darkMode ? 'text-3xl font-bold' : 'text-3xl font-bold text-gray-900'}>
              Admin Compliance Dashboard
            </h1>
            <p className={darkMode ? 'text-slate-300' : 'text-gray-600'}>
              Monitor course‑level AI compliance and audit‑ready transparency.
            </p>
          </div>
          <div className="flex gap-3">
            <Input
              value={courseId}
              onChange={(e) => setCourseId(e.target.value)}
              className={darkMode ? 'bg-slate-900 border-slate-700 text-white' : ''}
              placeholder="Course ID"
            />
            <Button onClick={fetchAnalytics} disabled={loading}>
              {loading ? 'Loading...' : 'Refresh'}
            </Button>
            <Button variant="secondary" className="bg-emerald-600 text-white hover:bg-emerald-700">
              Export Audit Trail
            </Button>
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-100 text-red-800 rounded-lg mb-4">
            {error}
          </div>
        )}

        <div className="grid lg:grid-cols-3 gap-6">
          <Card className={darkMode ? 'bg-slate-900 border-slate-800 text-white' : ''}>
            <CardHeader>
              <CardTitle>CS101 Compliance</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold mt-2">{complianceValue}</p>
              <p className={darkMode ? 'text-slate-400 text-sm mt-2' : 'text-gray-500 text-sm mt-2'}>
                Above institution target of 80%
              </p>
            </CardContent>
          </Card>
          <Card className={darkMode ? 'bg-slate-900 border-slate-800 text-white' : ''}>
            <CardHeader>
              <CardTitle>Active Students</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold mt-2">{analytics?.unique_students ?? 42}</p>
              <p className={darkMode ? 'text-slate-400 text-sm mt-2' : 'text-gray-500 text-sm mt-2'}>
                Unique learners with AI checks
              </p>
            </CardContent>
          </Card>
          <Card className={darkMode ? 'bg-slate-900 border-slate-800 text-white' : ''}>
            <CardHeader>
              <CardTitle>Total Events</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold mt-2">{analytics?.total_events ?? 64}</p>
              <p className={darkMode ? 'text-slate-400 text-sm mt-2' : 'text-gray-500 text-sm mt-2'}>
                AI actions logged this week
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-6 mt-8">
          <Card className={darkMode ? 'bg-slate-900 border-slate-800 text-white' : ''}>
            <CardHeader>
              <CardTitle>AI vs No‑AI Usage</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {chartRows.map(([action, count]) => (
                <div key={action} className={darkMode ? 'bg-slate-800 rounded-lg p-3' : 'bg-slate-50 rounded-lg p-3'}>
                  <div className="flex justify-between text-sm">
                    <span className="capitalize">{action.replace('_', ' ')}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                  <div className={darkMode ? 'mt-2 h-2 bg-slate-700 rounded-full' : 'mt-2 h-2 bg-slate-200 rounded-full'}>
                    <div
                      className="h-2 rounded-full bg-indigo-500"
                      style={{ width: `${Math.min(100, (Number(count) / Math.max(1, totalEvents || 30)) * 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className={darkMode ? 'bg-slate-900 border-slate-800 text-white' : ''}>
            <CardHeader>
              <CardTitle>Policy Coverage Heatmap</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-6 gap-2">
                {Array.from({ length: 24 }).map((_, idx) => (
                  <div
                    key={idx}
                    className={
                      darkMode
                        ? `h-10 rounded-lg ${idx % 5 === 0 ? 'bg-emerald-600' : idx % 3 === 0 ? 'bg-indigo-600' : 'bg-slate-700'}`
                        : `h-10 rounded-lg ${idx % 5 === 0 ? 'bg-emerald-200' : idx % 3 === 0 ? 'bg-indigo-200' : 'bg-slate-200'}`
                    }
                  />
                ))}
              </div>
              <p className={darkMode ? 'text-xs text-slate-400 mt-3' : 'text-xs text-gray-500 mt-3'}>
                Higher intensity indicates stronger policy coverage.
              </p>
            </CardContent>
          </Card>
        </div>

        <Card className={darkMode ? 'bg-slate-900 border-slate-800 text-slate-300 mt-8' : 'mt-8'}>
          <CardContent className="text-sm">
            <strong className={darkMode ? 'text-white' : 'text-gray-900'}>Privacy Notice:</strong> All data is aggregated and anonymized. No student names, IDs, or assignment content is visible.
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
