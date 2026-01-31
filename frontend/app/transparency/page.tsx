'use client';

import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

interface LogData {
  summary: string;
  aggregates?: Array<{
    action: string;
    count: number;
  }>;
}

export default function TransparencyPage() {
  const [pseudonym, setPseudonym] = useState('student_123');
  const [courseId, setCourseId] = useState('CS101');
  const [logData, setLogData] = useState<LogData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.get(
        `${API_BASE}/api/transparency/my-logs/${pseudonym}?course_id=${courseId}`
      );
      setLogData(response.data);
    } catch (err: unknown) {
      const error = err as { message?: string };
      setError(`Failed to load logs: ${error.message ?? 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  }, [courseId, pseudonym]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 p-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center gap-3 mb-6">
            <span className="text-3xl">👁️</span>
            <h1 className="text-3xl font-bold text-gray-800">Your AI Use Log</h1>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-green-800">
              ✅ <strong>Privacy Safe:</strong> We only log what you did, not what you created. No personal data stored.
            </p>
          </div>

          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Pseudonym (Your Safe ID)
              </label>
              <input
                type="text"
                value={pseudonym}
                onChange={(e) => setPseudonym(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="e.g., student_123"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Course ID
              </label>
              <input
                type="text"
                value={courseId}
                onChange={(e) => setCourseId(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="e.g., CS101"
              />
            </div>

            <button
              onClick={fetchLogs}
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-lg transition"
            >
              {loading ? 'Loading...' : 'View My Logs'}
            </button>
          </div>

          {error && (
            <div className="p-4 bg-red-100 text-red-800 rounded-lg mb-4">
              {error}
            </div>
          )}

          {logData && (
            <div className="space-y-6">
              <div className="border-t pt-6">
                <p className="text-lg font-semibold text-gray-800">
                  {logData.summary}
                </p>
              </div>

              {logData.aggregates && logData.aggregates.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-3">
                    Breakdown by Action:
                  </h3>
                  <div className="space-y-2">
                    {logData.aggregates.map((agg, idx) => (
                      <div
                        key={idx}
                        className="flex justify-between items-center bg-gray-50 p-3 rounded"
                      >
                        <span className="text-gray-700 capitalize">
                          {agg.action}
                        </span>
                        <span className="font-semibold text-gray-900">
                          {agg.count} event{agg.count !== 1 ? 's' : ''}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
                <strong>Privacy Guarantee:</strong><br/>
                • No assignment content logged<br/>
                • No personal information stored<br/>
                • Logs auto-delete after 90 days<br/>
                • Only you and admins see this
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
