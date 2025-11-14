import { useEffect, useState } from 'react';

export function AnimatedBackground() {
  const [particles, setParticles] = useState<Array<{ id: number; x: number; delay: number; duration: number }>>([]);

  useEffect(() => {
    // Generate random particles
    const particleArray = Array.from({ length: 15 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      delay: Math.random() * 5,
      duration: 8 + Math.random() * 8,
    }));
    setParticles(particleArray);
  }, []);

  return (
    <div className="fixed inset-0 z-[5] pointer-events-none overflow-hidden">
      {/* Floating Particles */}
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute w-1 h-1 bg-cyan-400/40 rounded-full animate-float"
          style={{
            left: `${particle.x}%`,
            bottom: '-10px',
            animationDelay: `${particle.delay}s`,
            animationDuration: `${particle.duration}s`,
          }}
        />
      ))}

      {/* Bubbling Flask - Bottom Left */}
      <div className="absolute bottom-8 left-8 hidden lg:block">
        <div className="relative w-16 h-20">
          {/* Flask body */}
          <div className="absolute bottom-0 w-16 h-16 bg-gradient-to-t from-emerald-500/20 to-emerald-400/10 border-2 border-emerald-400/40 rounded-b-full" 
            style={{ imageRendering: 'pixelated' }}
          />
          {/* Flask neck */}
          <div className="absolute bottom-12 left-1/2 -translate-x-1/2 w-6 h-8 bg-emerald-500/10 border-2 border-emerald-400/40 border-b-0"
            style={{ imageRendering: 'pixelated' }}
          />
          
          {/* Bubbles */}
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-emerald-300/60 rounded-full animate-bubble"
              style={{
                left: `${30 + i * 15}%`,
                bottom: '10px',
                animationDelay: `${i * 0.8}s`,
              }}
            />
          ))}
        </div>
      </div>

      {/* Blinking Monitor Light - Top Right */}
      <div className="absolute top-24 right-12 hidden xl:block">
        <div className="flex gap-2">
          <div className="w-3 h-3 bg-red-500 rounded-sm animate-blink-slow"
            style={{ imageRendering: 'pixelated', animationDelay: '0s' }}
          />
          <div className="w-3 h-3 bg-emerald-500 animate-blink-slow"
            style={{ imageRendering: 'pixelated', animationDelay: '0.5s' }}
          />
          <div className="w-3 h-3 bg-yellow-500 animate-blink-slow"
            style={{ imageRendering: 'pixelated', animationDelay: '1s' }}
          />
        </div>
      </div>

      {/* Floating Chemical Symbols */}
      <div className="absolute top-1/4 right-1/4 hidden lg:block animate-float-slow">
        <div className="text-2xl text-cyan-400/30 font-mono" style={{ imageRendering: 'pixelated' }}>
          H₂O
        </div>
      </div>

      <div className="absolute top-2/3 left-1/4 hidden lg:block animate-float-slow" style={{ animationDelay: '2s' }}>
        <div className="text-2xl text-purple-400/30 font-mono" style={{ imageRendering: 'pixelated' }}>
          NaCl
        </div>
      </div>

      {/* Pixel-style scan lines for retro effect */}
      <div 
        className="absolute inset-0 pointer-events-none opacity-[0.02]"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.3) 2px, rgba(0,0,0,0.3) 4px)',
        }}
      />
    </div>
  );
}
