import { Beaker } from 'lucide-react';

export function Header() {
  return (
    <header className="border-b-3 border-cyan-500/40 bg-slate-900/80 backdrop-blur-sm relative overflow-hidden" style={{ imageRendering: 'pixelated' }}>
      {/* Pixel grid effect */}
      <div className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: 'repeating-linear-gradient(90deg, transparent, transparent 8px, rgba(6,182,212,0.5) 8px, rgba(6,182,212,0.5) 10px), repeating-linear-gradient(0deg, transparent, transparent 8px, rgba(6,182,212,0.5) 8px, rgba(6,182,212,0.5) 10px)',
        }}
      />
      
      <div className="container mx-auto px-4 py-4 max-w-6xl relative z-10">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyan-500/30 border-3 border-cyan-400/60 relative group"
            style={{ imageRendering: 'pixelated' }}
          >
            <Beaker className="w-5 h-5 text-cyan-300" strokeWidth={2.5} />
            <div className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-cyan-400 animate-pulse" />
          </div>
          <div>
            <h1 className="text-base text-cyan-300 tracking-wider pixel-text drop-shadow-[0_0_10px_rgba(103,232,249,0.5)]">
              Chemical Formula Optimizer
            </h1>
            <p className="text-xs text-cyan-200/80 font-mono">
              ▸ Ingredient Input & Optimization System
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}