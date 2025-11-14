import signatureImage from 'figma:asset/d63227c3ab9c7305aab730334ca806c2c51c9924.png';

export function Signature() {
  return (
    <footer className="border-t-3 border-cyan-500/40 bg-slate-900/80 backdrop-blur-sm py-4 relative overflow-hidden">
      {/* Animated scan line */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-cyan-400/60 to-transparent animate-scan" />
      
      {/* Pixel grid effect */}
      <div className="absolute inset-0 opacity-5"
        style={{
          backgroundImage: 'repeating-linear-gradient(90deg, transparent, transparent 8px, rgba(6,182,212,0.5) 8px, rgba(6,182,212,0.5) 10px), repeating-linear-gradient(0deg, transparent, transparent 8px, rgba(6,182,212,0.5) 8px, rgba(6,182,212,0.5) 10px)',
        }}
      />
      
      <div className="container mx-auto px-4 max-w-6xl flex justify-center relative z-10">
        <div className="relative">
          <img 
            src={signatureImage} 
            alt="Victor Gomes - ciência em cada detalhe"
            className="h-16 object-contain opacity-90 drop-shadow-[0_0_20px_rgba(103,232,249,0.3)]"
            style={{ imageRendering: 'pixelated' }}
          />
          {/* Decorative corner indicators */}
          <div className="absolute -top-1 -left-1 w-2 h-2 border-t-2 border-l-2 border-cyan-400 animate-pulse" />
          <div className="absolute -top-1 -right-1 w-2 h-2 border-t-2 border-r-2 border-cyan-400 animate-pulse" style={{ animationDelay: '0.5s' }} />
          <div className="absolute -bottom-1 -left-1 w-2 h-2 border-b-2 border-l-2 border-cyan-400 animate-pulse" style={{ animationDelay: '1s' }} />
          <div className="absolute -bottom-1 -right-1 w-2 h-2 border-b-2 border-r-2 border-cyan-400 animate-pulse" style={{ animationDelay: '1.5s' }} />
        </div>
      </div>
    </footer>
  );
}