import { useState } from 'react';
import { IngredientList } from './components/IngredientList';
import { Header } from './components/Header';
import { Signature } from './components/Signature';
import { AnimatedBackground } from './components/AnimatedBackground';
import labBackground from 'figma:asset/2bca9c3206bb9204d98c0ad5e25416c6d83c7faf.png';

export default function App() {
  return (
    <div className="min-h-screen relative overflow-hidden bg-[#2a5568]">
      {/* Pixel Art Laboratory Background */}
      <div 
        className="fixed inset-0 z-0"
        style={{
          backgroundImage: `url(${labBackground})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          imageRendering: 'pixelated',
        }}
      />
      
      {/* Dark overlay for better contrast */}
      <div className="fixed inset-0 z-0 bg-gradient-to-b from-slate-900/70 via-slate-900/85 to-slate-950/90" />
      
      {/* Animated Elements */}
      <AnimatedBackground />
      
      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        <Header />
        
        <main className="flex-1 container mx-auto px-4 py-6 max-w-6xl">
          <IngredientList />
        </main>
        
        <Signature />
      </div>
    </div>
  );
}