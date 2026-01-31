'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export default function MobilePolicyCheck() {
  const [courseId, setCourseId] = useState('CS101');
  const [action, setAction] = useState('Brainstorm');
  const [allowed, setAllowed] = useState(true);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white flex flex-col items-center justify-center p-6">
      <Card className="w-full max-w-xs bg-black/80 border-slate-700 rounded-[36px] shadow-2xl text-white">
        <CardHeader className="flex-row items-center justify-between">
          <div>
            <p className="text-xs text-slate-400">EVGG Mobile</p>
            <CardTitle className="text-lg">Policy Check</CardTitle>
          </div>
          <Badge className="bg-emerald-600/20 text-emerald-300">Live</Badge>
        </CardHeader>

        <CardContent className="space-y-4">
          <div>
            <label className="text-xs text-slate-400">Course</label>
            <Select value={courseId} onValueChange={setCourseId}>
              <SelectTrigger className="mt-1 bg-slate-800 text-white border-slate-700">
                <SelectValue placeholder="Select course" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="CS101">CS101</SelectItem>
                <SelectItem value="ENG102">ENG102</SelectItem>
                <SelectItem value="BIO110">BIO110</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="text-xs text-slate-400">Action</label>
            <Select
              value={action}
              onValueChange={(value) => {
                setAction(value);
                setAllowed(value !== 'Full Solution');
              }}
            >
              <SelectTrigger className="mt-1 bg-slate-800 text-white border-slate-700">
                <SelectValue placeholder="Select action" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Brainstorm">Brainstorm</SelectItem>
                <SelectItem value="Code Review">Code Review</SelectItem>
                <SelectItem value="Full Solution">Full Solution</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className={`text-center py-4 rounded-2xl font-bold text-lg ${allowed ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}`}>
            {allowed ? '✅ ALLOWED' : '❌ BANNED'}
          </div>

          <div className="bg-slate-800/70 p-3 rounded-lg text-xs text-slate-300">
            <p className="font-semibold text-slate-100 mb-1">Disclosure Instructions</p>
            If AI was used, include: “I used AI for brainstorming; final submission is my own work.”
          </div>

          <Button className="w-full" variant="default">
            Submit Check
          </Button>
        </CardContent>
      </Card>

      <Link href="/" className="text-xs text-slate-300 mt-6 hover:text-white">
        Back to desktop
      </Link>
    </div>
  );
}
