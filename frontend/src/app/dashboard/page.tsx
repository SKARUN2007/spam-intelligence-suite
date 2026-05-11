'use client';

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart3, Shield, Mail, AlertTriangle, Clock, ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';
import Link from 'next/link';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get(`${API_URL}/stats`);
        setStats(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div className="container">Loading Dashboard Intelligence...</div>;

  return (
    <main className="container" style={{ justifyContent: 'flex-start', paddingTop: '5rem' }}>
      <nav style={{ width: '100%', maxWidth: '1000px', marginBottom: '2rem' }}>
        <Link href="/" style={{ color: '#888', display: 'flex', alignItems: 'center', gap: '0.5rem', textDecoration: 'none' }}>
          <ArrowLeft size={16} /> Back to Scanner
        </Link>
      </nav>

      <div style={{ width: '100%', maxWidth: '1000px' }}>
        <h1 style={{ marginBottom: '2rem', fontSize: '2.5rem' }}>Security Intelligence <span style={{ color: 'var(--accent)' }}>Dashboard</span></h1>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '3rem' }}>
          <div className="card" style={{ padding: '1.5rem' }}>
            <div style={{ color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>Total Processed</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
              <Mail className="text-accent" /> {stats.total_scans}
            </div>
          </div>
          <div className="card" style={{ padding: '1.5rem' }}>
            <div style={{ color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>Threats Blocked</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--spam)', display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
              <AlertTriangle /> {stats.total_spam}
            </div>
          </div>
          <div className="card" style={{ padding: '1.5rem' }}>
            <div style={{ color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>Safety Ratio</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--ham)', display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
              <Shield /> {stats.total_scans > 0 ? Math.round((stats.total_ham / stats.total_scans) * 100) : 0}%
            </div>
          </div>
        </div>

        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem', color: '#888' }}>Recent Activity Log</h2>
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead style={{ background: 'rgba(255,255,255,0.02)', fontSize: '0.8rem', color: '#666', textTransform: 'uppercase' }}>
              <tr>
                <th style={{ padding: '1rem' }}>Timestamp</th>
                <th style={{ padding: '1rem' }}>Classification</th>
                <th style={{ padding: '1rem' }}>Confidence</th>
                <th style={{ padding: '1rem' }}>Status</th>
              </tr>
            </thead>
            <tbody style={{ fontSize: '0.9rem' }}>
              {stats.recent_scans.map((scan: any) => (
                <tr key={scan.id} style={{ borderTop: '1px solid var(--card-border)' }}>
                  <td style={{ padding: '1rem', color: '#888' }}><Clock size={14} style={{ marginRight: '0.4rem' }} /> {new Date(scan.timestamp).toLocaleString()}</td>
                  <td style={{ padding: '1rem', fontWeight: 'bold', textTransform: 'capitalize' }}>{scan.label}</td>
                  <td style={{ padding: '1rem' }}>{scan.confidence}%</td>
                  <td style={{ padding: '1rem' }}>
                    <span style={{ padding: '0.2rem 0.6rem', borderRadius: '4px', background: scan.is_spam ? 'rgba(255,77,77,0.1)' : 'rgba(0,230,118,0.1)', color: scan.is_spam ? 'var(--spam)' : 'var(--ham)', fontSize: '0.75rem' }}>
                      {scan.is_spam ? 'BLOCKED' : 'CLEARED'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
