'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

function Header() {
  const [backendStatus, setBackendStatus] = useState('checking...');
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await fetch('http://localhost:8000/health', {
          signal: AbortSignal.timeout(2000),
        });
        if (res.ok) {
          setBackendStatus('online');
          setIsOnline(true);
        } else {
          setBackendStatus('offline');
          setIsOnline(false);
        }
      } catch {
        setBackendStatus('offline');
        setIsOnline(false);
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="bg-white/80 backdrop-blur shadow-sm sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center" aria-label="Primary">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 animate-pulse" aria-hidden="true" />
          <div>
            <p className="text-xl font-bold text-gray-900">EVGG</p>
            <p className="text-xs text-gray-500">AI Governance Platform</p>
          </div>
        </div>
        <div className="flex gap-6 text-sm font-semibold items-center">
          <Link href="/policies" className="text-gray-700 hover:text-indigo-700 transition-colors">
            Faculty Builder
          </Link>
          <Link href="/copilot" className="text-gray-700 hover:text-indigo-700 transition-colors">
            Student Copilot
          </Link>
          <Link href="/dashboard" className="text-gray-700 hover:text-indigo-700 transition-colors">
            Student Dashboard
          </Link>
          <Link href="/admin" className="text-gray-700 hover:text-indigo-700 transition-colors">
            Admin Analytics
          </Link>
          <div className="flex items-center gap-2">
            <div className={`h-2 w-2 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
            <span className={`text-xs font-medium ${isOnline ? 'text-emerald-600' : 'text-red-600'}`}>
              {backendStatus}
            </span>
          </div>
        </div>
      </nav>
    </header>
  );
}

function Hero() {
  return (
    <section className="grid lg:grid-cols-2 gap-12 items-center animate-in fade-in duration-700">
      <div>
        <Badge variant="secondary" className="mb-6 gap-2 animate-in slide-in-from-left duration-500">
          <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
          Trusted by academic integrity teams
        </Badge>
        <h1 id="hero-title" className="text-5xl font-bold text-gray-900 leading-tight animate-in slide-in-from-left duration-700 delay-100">
          Executable AI Policies for Higher Education
        </h1>
        <p className="text-lg text-gray-700 mt-6 animate-in slide-in-from-left duration-700 delay-200">
          Turn PDF policies into automatic enforcement, verified Q&A, and
          privacy‑safe transparency.
        </p>

        <div className="mt-8 flex flex-wrap gap-3 animate-in slide-in-from-left duration-700 delay-300">
          <Badge variant="outline">✅ GDPR Compliant</Badge>
          <Badge variant="outline">✅ FERPA Ready</Badge>
          <Badge variant="outline">✅ Audit‑Ready Logs</Badge>
        </div>

        <div className="mt-10 flex flex-wrap gap-4 animate-in slide-in-from-left duration-700 delay-500">
          <Button asChild size="lg" className="hover:scale-105 transition-transform">
            <Link href="/policies">Start Free Trial</Link>
          </Button>
          <Button asChild size="lg" variant="outline" className="hover:scale-105 transition-transform">
            <Link href="/test">Run Live Demo</Link>
          </Button>
        </div>
      </div>

      <PolicyStatusCards />
    </section>
  );
}

function PolicyStatusCards() {
  const [allowedCount, setAllowedCount] = useState(12);
  const [restrictedCount, setRestrictedCount] = useState(5);
  const [compliance, setCompliance] = useState(98);

  useEffect(() => {
    // Simulate real-time metric updates
    const interval = setInterval(() => {
      setAllowedCount((prev) => prev + Math.floor(Math.random() * 3) - 1);
      setRestrictedCount((prev) => Math.max(0, prev + Math.floor(Math.random() * 2) - 1));
      setCompliance((prev) => Math.min(100, Math.max(90, prev + Math.floor(Math.random() * 4) - 2)));
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="border-blue-100 shadow-xl animate-in fade-in slide-in-from-right duration-500">
      <CardHeader className="flex-row items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Policy Status</p>
          <CardTitle>CS101 AI Policy</CardTitle>
        </div>
        <Badge className="bg-emerald-100 text-emerald-700 hover:bg-emerald-100 animate-pulse">Active</Badge>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-3 gap-4">
          <Card className="bg-blue-50 hover:bg-blue-100 transition-colors">
            <CardContent className="p-4">
              <p className="text-xs text-gray-600">Allowed</p>
              <p className="text-2xl font-bold text-blue-700 animate-pulse">{allowedCount}</p>
            </CardContent>
          </Card>
          <Card className="bg-purple-50 hover:bg-purple-100 transition-colors">
            <CardContent className="p-4">
              <p className="text-xs text-gray-600">Restricted</p>
              <p className="text-2xl font-bold text-purple-700 animate-pulse">{restrictedCount}</p>
            </CardContent>
          </Card>
          <Card className="bg-emerald-50 hover:bg-emerald-100 transition-colors">
            <CardContent className="p-4">
              <p className="text-xs text-gray-600">Compliance</p>
              <p className="text-2xl font-bold text-emerald-700 animate-pulse">{compliance}%</p>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-3 text-sm">
          {[
            { label: 'Verified Q&A', value: 'Enabled', color: 'text-emerald-600' },
            { label: 'Auto Enforcement', value: 'On', color: 'text-blue-600' },
            { label: 'Audit Logs', value: 'Active', color: 'text-purple-600' },
          ].map((item) => (
            <div key={item.label} className="flex items-center justify-between bg-gray-50 px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors">
              <span className="text-gray-700">{item.label}</span>
              <span className={`${item.color} font-semibold animate-pulse`}>{item.value}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function Features() {
  return (
    <section className="grid md:grid-cols-3 gap-6 mt-16">
      {[
        {
          title: 'Verified Q&A',
          body: 'Students get policy‑backed answers with citations and disclosure templates.',
        },
        {
          title: 'Enforcement',
          body: 'Real‑time allow/deny decisions for assignments, labs, and exams.',
        },
        {
          title: 'Audit Logs',
          body: 'Privacy‑safe transparency with anonymized logs for compliance teams.',
        },
      ].map((feature, idx) => (
        <Card key={feature.title} className="border-blue-50 hover:shadow-lg transition-shadow animate-in fade-in duration-700" style={{ animationDelay: `${idx * 100}ms` }}>
          <CardHeader>
            <CardTitle className="text-lg">{feature.title}</CardTitle>
          </CardHeader>
          <CardContent className="text-gray-700">
            {feature.body}
          </CardContent>
        </Card>
      ))}
    </section>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Header />
      <main className="max-w-7xl mx-auto px-8 py-20" aria-labelledby="hero-title">
        <Hero />
        <Features />
      </main>
    </div>
  );
}
