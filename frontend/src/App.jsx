import React, { useState, useEffect, useRef } from 'react';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [resumeLabel, setResumeLabel] = useState('Select File');
  const [jdLabel, setJdLabel] = useState('Select File');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [animatedScore, setAnimatedScore] = useState(0);
  const resultsRef = useRef(null);

  const handleFileChange = (e, type) => {
    const file = e.target.files[0];
    if (file) {
      if (type === 'resume') {
        setResumeFile(file);
        setResumeLabel(file.name);
      } else {
        setJdFile(file);
        setJdLabel(file.name);
      }
    }
  };

  const analyzeSkills = async () => {
    if (!resumeFile || !jdFile) {
      alert("Please provide both dossiers for analysis.");
      return;
    }

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('jd', jdFile);

    setIsLoading(true);
    setResults(null);

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.error) {
        alert(data.error);
      } else {
        setResults(data);
        // Animate score
        let start = 0;
        const end = data.score;
        const duration = 1500;
        const increment = end / (duration / 15);
        const timer = setInterval(() => {
          start += increment;
          if (start >= end) {
            setAnimatedScore(end);
            clearInterval(timer);
          } else {
            setAnimatedScore(Math.floor(start));
          }
        }, 15);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Convergence interrupted. Ensure the terminal is active.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (results && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [results]);

  return (
    <div className="bg-surface text-on-surface font-body selection:bg-primary-container selection:text-primary min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-[#121412] flex justify-between items-center px-8 py-6 border-b border-white/5">
        <div className="text-2xl font-headline text-primary tracking-tighter italic">Job Skill Gap Analyzer</div>
        <div className="hidden md:flex items-center gap-10">
          <a className="text-on-surface hover:text-primary transition-colors duration-300 font-label text-[10px] uppercase tracking-[0.2em]" href="#hero">Analysis</a>
          <a className="text-on-surface hover:text-primary transition-colors duration-300 font-label text-[10px] uppercase tracking-[0.2em]" href="#results-section">Results</a>
        </div>
      </nav>

      <main className="pt-32 pb-24">
        {/* Hero Section */}
        <section id="hero" className="px-8 md:px-20 mb-32">
          <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-8 items-end">
            <div className="md:col-span-8">
              <span className="font-headline italic text-primary text-xl md:text-2xl mb-6 block">/01 Skill Evaluation</span>
              <h1 className="font-headline text-5xl md:text-7xl leading-[1.1] tracking-tight text-on-surface">
                Understand Your <span className="italic text-primary">Skills</span> <br /> & Improve Your Resume.
              </h1>
            </div>
            <div className="md:col-span-4 pb-4">
              <p className="font-body text-on-surface-variant text-lg leading-relaxed max-w-sm">
                Upload your resume and job description to instantly analyze your skill match, identify gaps, and get actionable suggestions to improve your chances.
              </p>
            </div>
          </div>
        </section>

        {/* Upload Section */}
        <section className="mb-40 px-8 md:px-20">
          <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12">
            <div className="group relative bg-surface-container hover:bg-surface-container-high p-12 rounded-lg transition-all duration-500 border border-outline-variant/10">
              <h2 className="font-headline text-3xl mb-4 italic">Upload Resume</h2>
              <p className="text-on-surface-variant mb-8 font-light">Upload your resume in PDF format.</p>
              <input 
                type="file" 
                id="resume" 
                accept=".pdf" 
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                onChange={(e) => handleFileChange(e, 'resume')}
              />
              <div className={`text-xs uppercase tracking-widest border-b border-primary/30 inline-block pb-1 ${resumeFile ? 'text-on-surface' : 'text-primary'}`}>
                {resumeLabel}
              </div>
            </div>
            <div className="group relative bg-surface-container hover:bg-surface-container-high p-12 rounded-lg transition-all duration-500 border border-outline-variant/10">
              <h2 className="font-headline text-3xl mb-4 italic">Upload Job Description</h2>
              <p className="text-on-surface-variant mb-8 font-light">Upload the job description you want to analyze..</p>
              <input 
                type="file" 
                id="jd" 
                accept=".pdf" 
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                onChange={(e) => handleFileChange(e, 'jd')}
              />
              <div className={`text-xs uppercase tracking-widest border-b border-primary/30 inline-block pb-1 ${jdFile ? 'text-on-surface' : 'text-primary'}`}>
                {jdLabel}
              </div>
            </div>
          </div>
          <div className="max-w-7xl mx-auto mt-12 text-center">
            <button 
              id="analyze-btn" 
              onClick={analyzeSkills}
              disabled={isLoading}
              className="px-12 py-5 bg-gradient-to-r from-primary to-primary-container text-on-primary font-label text-xs uppercase tracking-[0.3em] rounded-md hover:opacity-90 transition-all duration-300 shadow-xl shadow-primary/10 disabled:opacity-50"
            >
              {isLoading ? 'Analyzing...' : 'Analyze Resume'}
            </button>
          </div>
        </section>

        {/* Loading Overlay */}
        {isLoading && (
          <div id="loader" className="fixed inset-0 z-50 bg-surface/95 backdrop-blur-md flex flex-col items-center justify-center">
            <span className="material-symbols-outlined text-primary text-6xl animate-pulse mb-6">hourglass_empty</span>
            <p className="font-headline text-2xl italic text-on-surface animate-pulse">Analyzing your resume and job match...</p>
          </div>
        )}

        {/* Results Section */}
        {results && (
          <div id="results-section" ref={resultsRef}>
            {/* Score Block */}
            <section className="bg-surface-container-low py-32 px-8 md:px-20 mb-40">
              <div className="max-w-4xl mx-auto text-center">
                <span className="material-symbols-outlined text-primary-container text-6xl mb-8 block">analytics</span>
                <blockquote className="font-headline text-5xl md:text-8xl italic leading-relaxed text-on-surface mb-6">
                  <span className="text-primary">{animatedScore}</span>%
                </blockquote>
                <cite className="text-xs uppercase tracking-[0.4em] font-label text-primary">
                  — {results.matched.length} Synchronized out of {results.matched.length + results.missing.length} Requirements
                </cite>
              </div>
            </section>

            {/* Technical Divergence */}
            <section className="px-8 md:px-20 mb-40">
              <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-end mb-16 border-b border-outline-variant/10 pb-8">
                  <div>
                    <span className="font-headline italic text-primary text-xl md:text-2xl mb-2 block">/02 Skill Analysis</span>
                    <h2 className="font-headline text-4xl md:text-6xl tracking-tight">Skill Gap Overview.</h2>
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                  <div className="space-y-8">
                    <h3 className="font-headline text-2xl italic text-secondary">Synchronized Skills</h3>
                    <div className="flex flex-wrap gap-4">
                      {results.matched.length > 0 ? results.matched.map((s, i) => (
                        <span key={i} className="px-6 py-2 rounded-full font-label text-[10px] uppercase tracking-widest text-secondary bg-secondary/5 border border-secondary/10">{s}</span>
                      )) : <p className="italic text-on-surface-variant opacity-50">None found.</p>}
                    </div>
                  </div>
                  <div className="space-y-8">
                    <h3 className="font-headline text-2xl italic text-tertiary">Missing Requirements</h3>
                    <div className="flex flex-wrap gap-4">
                      {results.missing.length > 0 ? results.missing.map((s, i) => (
                        <span key={i} className="px-6 py-2 rounded-full font-label text-[10px] uppercase tracking-widest text-tertiary bg-tertiary/5 border border-tertiary/10">{s}</span>
                      )) : <p className="italic text-on-surface-variant opacity-50">None found.</p>}
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Recruiter Perspective */}
            <section className="px-8 md:px-20 mb-40">
              <div className="max-w-7xl mx-auto flex flex-col md:flex-row gap-12 items-start">
                <div className="w-full md:w-1/3">
                  <span className="font-headline italic text-primary text-xl block mb-6">/03 Perspective</span>
                  <h2 className="font-headline text-4xl mb-8 leading-tight">The <span className="italic">Recruiter's</span> Gaze.</h2>
                  <p className="text-on-surface-variant font-light leading-relaxed">These are the key skills missing from your resume based on the job requirements.</p>
                </div>
                <div className="w-full md:w-2/3 grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="bg-surface-container p-8 rounded-lg border border-secondary/10">
                    <h4 className="font-headline text-xl text-secondary italic mb-6">Foundational Strengths</h4>
                    <div className="space-y-4">
                      {results.recruiter_view.strengths.map((item, i) => (
                        <div key={i} className="flex gap-4 items-start">
                          <span className="text-primary opacity-50">/</span>
                          <p className="text-on-surface-variant font-light leading-relaxed">{item}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="bg-surface-container p-8 rounded-lg border border-error/10">
                    <h4 className="font-headline text-xl text-error italic mb-6">Areas to Improve</h4>
                    <div className="space-y-4">
                      {results.recruiter_view.weaknesses.map((item, i) => (
                        <div key={i} className="flex gap-4 items-start">
                          <span className="text-primary opacity-50">/</span>
                          <p className="text-on-surface-variant font-light leading-relaxed">{item}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Roadmap & Tips */}
            <section className="px-8 md:px-20 mb-40">
              <div className="max-w-7xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-12 gap-12">
                  <div className="md:col-span-12 mb-12 text-center">
                    <h2 className="font-headline text-[8vw] leading-none text-surface-container-highest tracking-tighter opacity-30 select-none uppercase">Improvement Plan</h2>
                  </div>
                  <div className="md:col-span-7">
                    <h3 className="font-headline text-4xl mb-12 italic border-b border-primary/20 pb-4">Strategic Roadmap</h3>
                    <div className="space-y-10">
                      {results.action_plan.map((step, index) => (
                        <div key={index} className="group">
                          <span className="font-label text-[10px] uppercase tracking-widest text-primary block mb-2 opacity-60 group-hover:opacity-100 transition-opacity">
                            Step {index + 1}
                          </span>
                          <p className="font-body text-lg text-on-surface-variant font-light group-hover:text-on-surface transition-colors">
                            {step}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="md:col-span-5">
                    <h3 className="font-headline text-4xl mb-12 italic border-b border-primary/20 pb-4">Personalized Tips</h3>
                    <div className="space-y-6">
                      {results.smart_tips.map((tip, i) => (
                        <div key={i} className="p-6 bg-surface-container-low border-l-2 border-primary/20 hover:border-primary transition-all duration-300">
                          <p className="text-on-surface-variant font-light leading-relaxed italic">"{tip}"</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Checklist Section */}
            <section className="px-8 md:px-20 mb-32">
              <div className="max-w-4xl mx-auto bg-surface-container-low p-12 md:p-20 rounded-lg relative overflow-hidden">
                <div className="absolute top-0 right-0 p-12 opacity-5">
                  <span className="material-symbols-outlined text-9xl">checklist</span>
                </div>
                <h2 className="font-headline text-4xl md:text-5xl mb-12 italic leading-tight">The Upgrade <span className="text-primary underline decoration-1 underline-offset-8">Protocol</span>.</h2>
                <div className="space-y-6">
                  {results.checklist.map((item, i) => (
                    <div key={i} className="flex items-center gap-6 group cursor-pointer hover:translate-x-2 transition-transform duration-300">
                      <span className="material-symbols-outlined text-primary/40 group-hover:text-primary transition-colors">circle</span>
                      <p className="text-on-surface-variant group-hover:text-on-surface transition-colors">{item}</p>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-[#0d0f0d] w-full py-20 px-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-12">
          <div className="font-headline italic text-lg text-primary">Job Skill Gap Analyzer.</div>
        </div>
      </footer>
    </div>
  );
}

export default App;
