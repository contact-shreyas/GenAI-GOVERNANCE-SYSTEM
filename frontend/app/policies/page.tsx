'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';

export default function CreatePolicy() {
  const [courseId, setCourseId] = useState('CS101');
  const [policyTitle, setPolicyTitle] = useState('AI Usage Policy');
  const [instructorName, setInstructorName] = useState('Dr. Rao');
  const [brainstormAllowed, setBrainstormAllowed] = useState(true);
  const [fullSolutionBanned, setFullSolutionBanned] = useState(true);
  const [examAllBanned, setExamAllBanned] = useState(true);
  const [disclosureRequired, setDisclosureRequired] = useState(true);

  const [result, setResult] = useState<{ policy_id?: string; status?: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const compilePayload = () => {
    const allowed_uses: string[] = [];
    const prohibited_practices: string[] = [];

    if (brainstormAllowed) allowed_uses.push('brainstorm');
    if (fullSolutionBanned) prohibited_practices.push('full_solution');
    if (examAllBanned) prohibited_practices.push('exam_ai_banned');

    return {
      course_id: courseId,
      instructor_name: instructorName,
      allowed_uses,
      prohibited_practices,
    };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await fetch('http://localhost:8000/api/policies/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(compilePayload()),
      });

      if (!res.ok) throw new Error('Failed to compile policy');
      const data = (await res.json()) as { policy_id?: string; status?: string };
      
      // Simulate streaming response with delay
      await new Promise(resolve => setTimeout(resolve, 500));
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <nav className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-8 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-indigo-600">
            EVGG
          </Link>
          <div className="flex gap-4">
            <Link href="/" className="text-gray-600 hover:text-gray-800">
              Home
            </Link>
            <Link href="/test" className="text-indigo-600 font-semibold">
              Test
            </Link>
          </div>
        </div>
      </nav>

      {/* Main */}
      <div className="max-w-6xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Faculty Policy Builder</h1>
          <p className="text-gray-600">
            Create academic AI policies with guardrails and instant preview.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          <form onSubmit={handleSubmit} className="lg:col-span-2 space-y-6">
            {/* Course Info */}
            <Card>
              <CardHeader>
                <CardTitle>Course Info</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Course
                    </label>
                    <Select value={courseId} onValueChange={setCourseId}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select course" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="CS101">CS101</SelectItem>
                        <SelectItem value="CS201">CS201</SelectItem>
                        <SelectItem value="ENG102">ENG102</SelectItem>
                        <SelectItem value="BIO110">BIO110</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Policy Title
                    </label>
                    <Input
                      value={policyTitle}
                      onChange={(e) => setPolicyTitle(e.target.value)}
                      placeholder="AI Usage Policy"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Instructor
                  </label>
                  <Input
                    value={instructorName}
                    onChange={(e) => setInstructorName(e.target.value)}
                    placeholder="Dr. Rao"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Assignment Rules */}
            <Card>
              <CardHeader>
                <CardTitle>Assignment Rules</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between bg-gray-50 px-4 py-3 rounded-lg">
                  <div>
                    <p className="text-sm font-semibold text-gray-800">Brainstorm</p>
                    <p className="text-xs text-gray-500">Idea generation, outlines, prompts</p>
                  </div>
                  <Switch checked={brainstormAllowed} onCheckedChange={setBrainstormAllowed} />
                </div>
                <div className="flex items-center justify-between bg-gray-50 px-4 py-3 rounded-lg">
                  <div>
                    <p className="text-sm font-semibold text-gray-800">Full Solution</p>
                    <p className="text-xs text-gray-500">Complete answers or full code</p>
                  </div>
                  <Switch checked={fullSolutionBanned} onCheckedChange={setFullSolutionBanned} />
                </div>
              </CardContent>
            </Card>

            {/* Exam Rules */}
            <Card>
              <CardHeader>
                <CardTitle>Exam Rules</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between bg-gray-50 px-4 py-3 rounded-lg">
                  <div>
                    <p className="text-sm font-semibold text-gray-800">All AI Banned</p>
                    <p className="text-xs text-gray-500">No AI use during exams or quizzes</p>
                  </div>
                  <Switch checked={examAllBanned} onCheckedChange={setExamAllBanned} />
                </div>
              </CardContent>
            </Card>

            {/* Disclosure */}
            <Card>
              <CardHeader>
                <CardTitle>Disclosure Settings</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">Require disclosure of AI assistance</span>
                  <Switch checked={disclosureRequired} onCheckedChange={setDisclosureRequired} />
                </div>
              </CardContent>
            </Card>

            {/* Submit */}
            <Button type="submit" disabled={loading} className="w-full" size="lg">
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Compiling policy...
                </span>
              ) : (
                'Save Policy v1.0'
              )}
            </Button>
          </form>

          {/* Preview */}
          <Card className="h-fit">
            <CardHeader className="flex-row items-center justify-between">
              <CardTitle>Policy Preview</CardTitle>
              <Badge variant="secondary">Draft</Badge>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              <div>
                <p className="text-gray-500">Course</p>
                <p className="font-semibold text-gray-800">{courseId} — {policyTitle}</p>
              </div>
              <div>
                <p className="text-gray-500">Instructor</p>
                <p className="font-semibold text-gray-800">{instructorName || 'TBD'}</p>
              </div>
              <div>
                <p className="text-gray-500">Assignments</p>
                <ul className="mt-2 space-y-2">
                  <li className="flex items-center gap-2">
                    <span className={brainstormAllowed ? 'text-green-600' : 'text-gray-400'}>✅</span>
                    Brainstorming allowed
                  </li>
                  <li className="flex items-center gap-2">
                    <span className={fullSolutionBanned ? 'text-red-600' : 'text-gray-400'}>❌</span>
                    Full solutions banned
                  </li>
                </ul>
              </div>
              <div>
                <p className="text-gray-500">Exams</p>
                <p className="font-semibold text-gray-800">
                  {examAllBanned ? 'All AI banned' : 'Instructor discretion'}
                </p>
              </div>
              <div>
                <p className="text-gray-500">Disclosure</p>
                <p className="font-semibold text-gray-800">
                  {disclosureRequired ? 'Required with template' : 'Optional'}
                </p>
              </div>
            </CardContent>

            {result && (
              <CardContent className="pt-0">
                <div className="mt-2 bg-green-50 border border-green-200 rounded-lg p-4 animate-in slide-in-from-bottom duration-500">
                  <p className="text-green-800 font-semibold flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                    Policy compiled ✅
                  </p>
                  <pre className="mt-2 text-xs text-green-900 overflow-auto bg-white rounded p-2 border border-green-100">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              </CardContent>
            )}

            {error && (
              <CardContent className="pt-0">
                <div className="mt-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                  Error: {error}
                </div>
              </CardContent>
            )}
          </Card>
        </div>

      </div>
    </div>
  );
}
