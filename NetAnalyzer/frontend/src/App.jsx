import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, BarElement } from 'chart.js';
import { Doughnut, Line, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, BarElement);

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

const CHART_COLORS = ['#00FF88', '#00D4FF', '#FF2D55', '#FFA500', '#A78BFA', '#4A5568'];

const chartBase = {
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { labels: { color: '#C9D1D9', font: { family: 'JetBrains Mono', size: 11 } } } },
  scales: {
    y: { ticks: { color: '#4A5568', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: 'rgba(28,42,58,0.8)' }, border: { color: '#1C2A3A' } },
    x: { ticks: { color: '#4A5568', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: 'rgba(28,42,58,0.8)' }, border: { color: '#1C2A3A' } }
  }
};

const doughnutOpts = {
  responsive: true, maintainAspectRatio: false, cutout: '72%',
  plugins: { legend: { position: 'right', labels: { color: '#C9D1D9', font: { family: 'JetBrains Mono', size: 11 }, padding: 16, boxWidth: 12 } } }
};

// ── Components ─────────────────────────────────────────────────────
function NavBar() {
  return (
    <header className="sticky top-0 z-50 border-b border-hv-border bg-hv-bg/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded border border-hv-green/40 bg-hv-green/10 flex items-center justify-center">
            <span className="text-hv-green font-mono font-bold text-xs">NA</span>
          </div>
          <span className="font-mono font-semibold text-hv-bright text-sm tracking-wide">NetAnalyzer</span>
          <span className="badge-green text-[10px]">v2.0</span>
        </div>
        <nav className="hidden md:flex items-center gap-6">
          {['Dashboard', 'Scanner', 'Threats', 'History'].map(n => (
            <a key={n} href={`#${n.toLowerCase()}`} className="nav-link">{n}</a>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-hv-green animate-pulse" />
          <span className="font-mono text-xs text-hv-muted">SYSTEM ONLINE</span>
        </div>
      </div>
    </header>
  );
}

function HeroSection({ onScanClick }) {
  return (
    <section className="relative bg-grid bg-hero-radial border-b border-hv-border overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 py-20 md:py-28">
        <div className="max-w-2xl">
          <div className="section-label mb-4">// NETWORK INTELLIGENCE PLATFORM</div>
          <h1 className="text-4xl md:text-5xl font-bold text-hv-bright leading-tight mb-4">
            Deep Packet<br />
            <span className="text-hv-green text-green-glow">Analysis Engine</span>
          </h1>
          <p className="text-hv-text text-lg leading-relaxed mb-8 max-w-xl">
            Upload a <code className="font-mono text-hv-cyan bg-hv-card px-1.5 py-0.5 rounded text-sm">.pcap</code> capture file and get instant protocol analysis, threat intelligence, and network topology insights powered by Scapy.
          </p>
          <div className="flex flex-wrap gap-3">
            <button onClick={onScanClick} className="btn-primary">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
              Upload &amp; Analyze
            </button>
            <a href="#features" className="btn-outline">View Capabilities</a>
          </div>
          <div className="flex flex-wrap gap-6 mt-10 pt-8 border-t border-hv-border">
            {[['Protocol Detection','TCP/UDP/HTTP/DNS/ICMP'],['Threat Engine','Port scan &amp; C2 detection'],['Data Store','MongoDB Atlas']].map(([t,d])=>(
              <div key={t}>
                <div className="font-mono text-xs text-hv-green mb-0.5">{t}</div>
                <div className="text-xs text-hv-muted" dangerouslySetInnerHTML={{__html:d}} />
              </div>
            ))}
          </div>
        </div>
      </div>
      {/* Decorative grid lines */}
      <div className="absolute right-0 top-0 w-96 h-full opacity-20 pointer-events-none hidden lg:block">
        {[...Array(6)].map((_,i)=><div key={i} className="absolute top-0 w-px h-full bg-hv-green/20" style={{right:`${i*60+40}px`}} />)}
        {[...Array(8)].map((_,i)=><div key={i} className="absolute left-0 w-full h-px bg-hv-green/10" style={{top:`${i*60+30}px`}} />)}
      </div>
    </section>
  );
}

function FeatureCards() {
  const features = [
    { icon:'⬡', label:'Protocol Analysis', desc:'Identify TCP, UDP, ICMP, DNS, HTTP traffic with precise byte-level breakdown.', color:'green' },
    { icon:'◈', label:'Threat Detection', desc:'Flag port scans, SYN floods, suspicious IPs, and lateral movement patterns.', color:'red' },
    { icon:'◇', label:'Top Talkers', desc:'Identify the most active connections and data volumes across all streams.', color:'cyan' },
    { icon:'○', label:'Traffic Timeline', desc:'Visualize packet activity over time to pinpoint traffic spikes and anomalies.', color:'amber' },
  ];
  return (
    <section id="features" className="max-w-7xl mx-auto px-6 py-16">
      <div className="section-label">// CAPABILITIES</div>
      <h2 className="text-2xl font-bold text-hv-bright mb-8">What the Engine Does</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 stagger">
        {features.map(f => (
          <div key={f.label} className="hv-card group">
            <div className={`text-2xl mb-4 font-mono text-hv-${f.color}`}>{f.icon}</div>
            <div className="font-semibold text-hv-bright mb-2 text-sm">{f.label}</div>
            <div className="text-xs text-hv-muted leading-relaxed">{f.desc}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

function UploadSection({ file, setFile, analyzing, onUpload, scanRef }) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);

  const onDrop = (e) => {
    e.preventDefault(); setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f && (f.name.endsWith('.pcap') || f.name.endsWith('.pcapng'))) setFile(f);
  };

  return (
    <section id="scanner" ref={scanRef} className="max-w-7xl mx-auto px-6 py-8">
      <div className="section-label">// TARGET ACQUISITION</div>
      <h2 className="text-2xl font-bold text-hv-bright mb-6">Upload Capture File</h2>
      <div
        className={`upload-zone ${dragging ? 'dragging' : ''}`}
        onDragOver={(e)=>{e.preventDefault();setDragging(true);}}
        onDragLeave={()=>setDragging(false)}
        onDrop={onDrop}
        onClick={()=>inputRef.current?.click()}
      >
        <input ref={inputRef} type="file" accept=".pcap,.pcapng" className="hidden" onChange={e=>setFile(e.target.files[0])} />
        <div className="font-mono text-4xl text-hv-border mb-4">⬆</div>
        {file ? (
          <div className="animate-fade-in">
            <div className="font-mono text-hv-green font-semibold">{file.name}</div>
            <div className="text-xs text-hv-muted mt-1">{(file.size/1024).toFixed(1)} KB · Ready to analyze</div>
          </div>
        ) : (
          <>
            <div className="font-mono text-hv-text font-medium mb-1">Drop .pcap / .pcapng here</div>
            <div className="text-xs text-hv-muted">or click to browse files</div>
          </>
        )}
      </div>
      <div className="flex gap-3 mt-4">
        <button onClick={onUpload} disabled={!file || analyzing} className="btn-primary disabled:opacity-40 disabled:cursor-not-allowed">
          {analyzing ? (
            <><span className="w-3.5 h-3.5 border-2 border-hv-bg border-t-transparent rounded-full animate-spin inline-block" /> Analyzing...</>
          ) : (
            <><span>▶</span> Initialize Scan</>
          )}
        </button>
        {file && !analyzing && (
          <button onClick={()=>setFile(null)} className="btn-outline">✕ Clear</button>
        )}
      </div>
    </section>
  );
}

function Terminal({ logs }) {
  const ref = useRef(null);
  useEffect(() => { if (ref.current) ref.current.scrollTop = ref.current.scrollHeight; }, [logs]);

  const typeMap = {
    success: { prefix: '[+]', cls: 'terminal-line-green' },
    error:   { prefix: '[-]', cls: 'terminal-line-red' },
    warn:    { prefix: '[!]', cls: 'terminal-line-amber' },
    info:    { prefix: '[*]', cls: 'terminal-line-cyan' },
    system:  { prefix: '[SYS]', cls: 'terminal-line-muted' },
  };

  return (
    <div className="terminal-window h-full">
      <div className="terminal-titlebar">
        <span className="terminal-dot bg-hv-red" />
        <span className="terminal-dot bg-hv-amber" />
        <span className="terminal-dot bg-hv-green" />
        <span className="font-mono text-xs text-hv-muted ml-2">analyzer.log</span>
      </div>
      <div ref={ref} className="terminal-body h-72 overflow-y-auto space-y-1">
        {logs.map((log, i) => {
          const t = typeMap[log.type] || typeMap.info;
          return (
            <div key={i} className={`flex gap-2 text-xs ${t.cls} animate-slide-in`}>
              <span className="text-hv-muted shrink-0">[{log.time}]</span>
              <span className="shrink-0 font-semibold">{t.prefix}</span>
              <span className="text-hv-text" dangerouslySetInnerHTML={{__html: log.msg}} />
            </div>
          );
        })}
        <div className="text-hv-green font-mono text-xs">
          <span className="text-hv-muted">$ </span>
          <span className="cursor-blink" />
        </div>
      </div>
    </div>
  );
}

function StatCard({ value, label, accent }) {
  const colors = { green:'text-hv-green', red:'text-hv-red', cyan:'text-hv-cyan', amber:'text-hv-amber', bright:'text-hv-bright' };
  return (
    <div className="hv-card text-center group animate-fade-in">
      <div className={`text-3xl font-bold font-mono ${colors[accent]||colors.bright} mb-1`}>{value}</div>
      <div className="text-[11px] font-mono text-hv-muted uppercase tracking-widest">{label}</div>
    </div>
  );
}

function ProtocolChart({ data }) {
  const chartData = {
    labels: Object.keys(data),
    datasets: [{ data: Object.values(data), backgroundColor: CHART_COLORS, borderWidth: 0, hoverOffset: 8 }]
  };
  return (
    <div className="hv-card">
      <div className="section-label">// PROTOCOL MAP</div>
      <h3 className="text-sm font-semibold text-hv-bright mb-4">Protocol Breakdown</h3>
      <div className="h-52"><Doughnut data={chartData} options={doughnutOpts} /></div>
      <div className="mt-4 space-y-2">
        {Object.entries(data).map(([k,v],i)=>{
          const total = Object.values(data).reduce((a,b)=>a+b,0);
          return (
            <div key={k} className="flex items-center gap-3">
              <span className="font-mono text-xs w-14 text-hv-text">{k}</span>
              <div className="flex-1 progress-track">
                <div className="progress-fill-green" style={{width:`${(v/total*100).toFixed(0)}%`, background: CHART_COLORS[i]}} />
              </div>
              <span className="font-mono text-xs text-hv-muted w-8 text-right">{v}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function TimelineChart({ timeline }) {
  const data = {
    labels: timeline.map((_,i)=>`${i}s`),
    datasets: [{ label:'Packets', data: timeline.map(t=>t.count), borderColor:'#00FF88', backgroundColor:'rgba(0,255,136,0.06)', fill:true, tension:0.4, pointRadius:0, borderWidth:2 }]
  };
  return (
    <div className="hv-card">
      <div className="section-label">// TEMPORAL ANALYSIS</div>
      <h3 className="text-sm font-semibold text-hv-bright mb-4">Network Activity Timeline</h3>
      <div className="h-52">
        <Line data={data} options={{...chartBase, plugins:{legend:{display:false}}}} />
      </div>
    </div>
  );
}

function SizeChart({ sizes }) {
  const data = {
    labels: Object.keys(sizes),
    datasets: [{ label:'Count', data: Object.values(sizes), backgroundColor:'rgba(0,212,255,0.6)', borderColor:'#00D4FF', borderWidth:1, borderRadius:4 }]
  };
  return (
    <div className="hv-card">
      <div className="section-label">// SIZE DISTRIBUTION</div>
      <h3 className="text-sm font-semibold text-hv-bright mb-4">Packet Size Histogram</h3>
      <div className="h-52">
        <Bar data={data} options={{...chartBase, plugins:{legend:{display:false}}}} />
      </div>
    </div>
  );
}

function ThreatPanel({ threats }) {
  if (!threats.length) {
    return (
      <div className="hv-card flex flex-col items-center justify-center py-10 text-center">
        <div className="text-3xl mb-3">✓</div>
        <div className="font-mono text-hv-green font-semibold text-sm mb-1">No Threats Detected</div>
        <div className="text-xs text-hv-muted">Traffic analysis found no immediate indicators of compromise.</div>
      </div>
    );
  }
  return (
    <div className="hv-card-red">
      <div className="section-label text-hv-red">// THREAT INTELLIGENCE</div>
      <h3 className="text-sm font-semibold text-hv-bright mb-4 flex items-center gap-2">
        <span className="text-hv-red">⚠</span> {threats.length} Threat{threats.length>1?'s':''} Detected
      </h3>
      <div className="space-y-3 max-h-64 overflow-y-auto">
        {threats.map((t,i)=>(
          <div key={i} className="bg-hv-red/5 border border-hv-red/20 rounded p-3 animate-fade-in">
            <div className="flex items-start justify-between gap-2 mb-1">
              <span className="badge-red">{t.type}</span>
              <span className="font-mono text-[10px] text-hv-muted shrink-0">SRC: {t.src}</span>
            </div>
            <p className="text-xs text-hv-muted mt-1">{t.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function TopTalkers({ talkers }) {
  return (
    <div className="hv-card">
      <div className="section-label">// NETWORK TOPOLOGY</div>
      <h3 className="text-sm font-semibold text-hv-bright mb-4">Top Communication Streams</h3>
      <div className="overflow-x-auto">
        <table className="hv-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Connection</th>
              <th>Protocol</th>
              <th className="text-right">Packets</th>
            </tr>
          </thead>
          <tbody>
            {talkers.map((t,i)=>(
              <tr key={i}>
                <td><span className="text-hv-muted">{String(i+1).padStart(2,'0')}</span></td>
                <td><span className="text-hv-cyan text-xs">{t.connection}</span></td>
                <td><span className="badge-green">{t.protocol}</span></td>
                <td className="text-right font-semibold text-hv-green">{t.count.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function HistorySection({ history }) {
  if (!history.length) return null;
  return (
    <section id="history" className="max-w-7xl mx-auto px-6 py-8 border-t border-hv-border">
      <div className="section-label">// ANALYSIS HISTORY</div>
      <h2 className="text-2xl font-bold text-hv-bright mb-6">Recent Scans</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 stagger">
        {history.map((h,i)=>(
          <div key={i} className="hv-card">
            <div className="flex items-start justify-between mb-2">
              <span className="font-mono text-xs text-hv-green truncate max-w-[70%]">{h.filename}</span>
              {h.threats_found > 0
                ? <span className="badge-red">{h.threats_found} threats</span>
                : <span className="badge-green">Clean</span>
              }
            </div>
            <div className="text-xs text-hv-muted font-mono">
              {new Date(h.timestamp).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

// ── Main App ───────────────────────────────────────────────────────
export default function App() {
  const [file, setFile]         = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults]   = useState(null);
  const [logs, setLogs]         = useState([]);
  const [history, setHistory]   = useState([]);
  const scanRef = useRef(null);

  const addLog = (msg, type='info') => {
    const time = new Date().toLocaleTimeString('en-GB', { hour12:false });
    setLogs(prev => [...prev, { msg, type, time }]);
  };

  useEffect(() => {
    addLog('NetAnalyzer v2.0 — Packet Inspection Engine ready', 'system');
    addLog('Waiting for target .pcap file...', 'system');
    axios.get(`${API_URL}/api/history`).then(r=>setHistory(r.data)).catch(()=>{});
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    const fd = new FormData();
    fd.append('pcapFile', file);
    setAnalyzing(true); setResults(null);
    addLog(`Target acquired: <strong>${file.name}</strong>`, 'warn');
    addLog('Spawning Scapy analysis engine...', 'info');
    try {
      const res = await axios.post(`${API_URL}/api/upload`, fd);
      setResults(res.data);
      addLog(`Processed <strong>${res.data.summary.total_packets.toLocaleString()}</strong> packets`, 'success');
      addLog(`Duration: ${res.data.summary.duration.toFixed(3)}s`, 'info');
      addLog(`Protocols detected: ${Object.keys(res.data.protocols).join(', ')}`, 'success');
      if (res.data.threats.length) {
        addLog(`⚠ ${res.data.threats.length} threat indicator(s) found!`, 'error');
      } else {
        addLog('No threats detected in capture.', 'success');
      }
      addLog('Dashboard rendered. Analysis complete.', 'success');
      axios.get(`${API_URL}/api/history`).then(r=>setHistory(r.data)).catch(()=>{});
    } catch (err) {
      addLog(`Analysis failed: ${err.response?.data?.error || err.message}`, 'error');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <NavBar />

      <HeroSection onScanClick={()=>scanRef.current?.scrollIntoView({behavior:'smooth'})} />
      <FeatureCards />

      <div className="max-w-7xl mx-auto w-full px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <UploadSection file={file} setFile={setFile} analyzing={analyzing} onUpload={handleUpload} scanRef={scanRef} />
          </div>
          <div className="pt-8 lg:pt-[6.5rem]">
            <Terminal logs={logs} />
          </div>
        </div>
      </div>

      {results && (
        <div id="threats" className="max-w-7xl mx-auto w-full px-6 pb-8 animate-fade-in">
          <hr className="hv-divider" />
          <div className="section-label">// ANALYSIS RESULTS</div>
          <h2 className="text-2xl font-bold text-hv-bright mb-6">Intelligence Report</h2>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 stagger">
            <StatCard value={results.summary.total_packets.toLocaleString()} label="Packets" accent="green" />
            <StatCard value={`${results.summary.duration.toFixed(2)}s`} label="Duration" accent="cyan" />
            <StatCard value={results.top_talkers.length} label="Streams" accent="bright" />
            <StatCard value={results.threats.length} label="Threat Flags" accent={results.threats.length > 0 ? 'red' : 'green'} />
          </div>

          {/* Charts Row 1 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <ProtocolChart data={results.protocols} />
            <SizeChart sizes={results.sizes} />
          </div>

          {/* Timeline */}
          <div className="mb-6">
            <TimelineChart timeline={results.timeline} />
          </div>

          {/* Threats + Top Talkers */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ThreatPanel threats={results.threats} />
            <TopTalkers talkers={results.top_talkers} />
          </div>
        </div>
      )}

      <HistorySection history={history} />

      <footer className="border-t border-hv-border mt-auto">
        <div className="max-w-7xl mx-auto px-6 py-6 flex flex-col sm:flex-row justify-between items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="font-mono font-bold text-hv-bright text-sm">NetAnalyzer</span>
            <span className="badge-green text-[10px]">v2.0</span>
          </div>
          <div className="font-mono text-xs text-hv-muted">
            React · Node.js · Python Scapy · MongoDB — Built for cybersecurity research
          </div>
          <div className="flex gap-4">
            <a href="https://github.com" target="_blank" rel="noreferrer" className="btn-ghost text-xs">GitHub</a>
            <a href="#scanner" className="btn-ghost text-xs">Upload Capture</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
