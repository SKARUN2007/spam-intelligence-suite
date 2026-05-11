'use client';

import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Shield, ShieldAlert, ShieldCheck, Search, Loader2, BarChart3, AlertCircle, Upload, FileText, Download, Eye, EyeOff, Globe, MapPin } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function SpamChecker() {
  const [text, setText] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [safeView, setSafeView] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const performScan = async (data: any, isFile = false) => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const config = { headers: { 'Content-Type': isFile ? 'multipart/form-data' : 'application/json' } };
      const response = await axios.post(`${API_URL}/${isFile ? 'upload' : 'predict'}`, data, config);
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis engine unreachable.');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!result?.scan_id) return;
    window.open(`${API_URL}/report/${result.scan_id}`, '_blank');
  };

  return (
    <main className="container">
      <nav style={{ position: 'absolute', top: '2rem', right: '2rem', display: 'flex', gap: '1rem' }}>
        <Link href="/dashboard" className="button" style={{ padding: '0.6rem 1.2rem', fontSize: '0.8rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--card-border)' }}>
          <BarChart3 size={14} /> Analytics
        </Link>
      </nav>

      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="hero">
        <div style={{ display: 'inline-block', padding: '0.5rem 1rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '100px', color: 'var(--accent)', fontSize: '0.7rem', fontWeight: 'bold', marginBottom: '1rem', border: '1px solid var(--accent)', letterSpacing: '0.1em' }}>
          MASTER CYBER-INTELLIGENCE v4.0
        </div>
        <h1 style={{ fontSize: '4rem' }}>Spam <span style={{ color: 'var(--accent)' }}>Forensics</span></h1>
      </motion.div>

      <div className="card">
        <div className="input-group" style={{ position: 'relative' }}>
          <div className="scanning-container">
            {safeView ? (
              <div style={{ width: '100%', minHeight: '180px', background: 'rgba(0,0,0,0.5)', borderRadius: '16px', padding: '1.5rem', fontSize: '0.9rem', color: '#00e676', fontFamily: 'monospace', border: '1px dashed #00e676' }}>
                [SAFE VIEW ACTIVE] - MALICIOUS SCRIPTS & LINKS STRIPPED<br/><br/>
                {text.replace(/http/g, '[LINK REMOVED]')}
              </div>
            ) : (
              <textarea
                placeholder="Paste content or drop .eml for forensics..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                disabled={loading}
                style={{ minHeight: '180px' }}
              />
            )}
            {loading && <div className="scanner-line" />}
          </div>
          <button onClick={() => setSafeView(!safeView)} style={{ position: 'absolute', bottom: '1rem', right: '1rem', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '8px', padding: '0.4rem 0.8rem', color: '#fff', fontSize: '0.7rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            {safeView ? <><Eye size={14} /> Normal View</> : <><EyeOff size={14} /> Safe View</>}
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
          <button className="button" onClick={() => performScan({ text })} disabled={loading || !text.trim()}>
             Run Forensics
          </button>
          <button className="button" style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid var(--card-border)' }} onClick={() => fileInputRef.current?.click()}>
            <Upload size={18} /> Deep File Scan
          </button>
          <input type="file" ref={fileInputRef} onChange={(e) => { const f = e.target.files?.[0]; if(f){ const d = new FormData(); d.append('file', f); performScan(d, true); } }} style={{ display: 'none' }} accept=".eml" />
        </div>

        <AnimatePresence>
          {result && (
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}>
              <div className={`result ${result.label}`} style={{ marginBottom: '1.5rem' }}>
                <div className="result-header" style={{ fontSize: '1.8rem' }}>
                  {result.is_spam ? <><ShieldAlert /> CRITICAL THREAT</> : <><ShieldCheck /> SECURE</>}
                </div>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginTop: '1rem' }}>
                   <span>Confidence: <b>{result.confidence}%</b></span>
                   {result.geo && <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}><MapPin size={14} /> {result.geo.country} {result.geo.flag}</span>}
                </div>
              </div>

              {result.homograph_alerts?.length > 0 && (
                <div style={{ padding: '1rem', background: 'rgba(255,77,77,0.1)', border: '1px solid var(--spam)', borderRadius: '12px', marginBottom: '1.5rem', color: 'var(--spam)', fontSize: '0.9rem' }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}><AlertCircle size={16}/> DOMAIN IMPERSONATION DETECTED</div>
                  {result.homograph_alerts.map((a:any, i:number) => (
                    <div key={i}>Alert: <b>{a.domain}</b> is attempting to mimic <b>{a.target}</b></div>
                  ))}
                </div>
              )}

              <button className="button" style={{ width: '100%', background: 'linear-gradient(90deg, #6366f1, #a855f7)' }} onClick={downloadReport}>
                <Download size={18} /> Download Security Audit Report (PDF)
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
