'use client';
import Image from 'next/image';
import { useEffect, useState } from 'react';
import { Personality } from '@/app/data/quiz';

interface QuizResultProps {
  personality: Personality;
  onRestart: () => void;
}

export default function QuizResult({ personality, onRestart }: QuizResultProps) {
  const [visible, setVisible] = useState(false);
  const [imgVisible, setImgVisible] = useState(false);
  const [textVisible, setTextVisible] = useState(false);

  useEffect(() => {
    setTimeout(() => setVisible(true), 50);
    setTimeout(() => setImgVisible(true), 300);
    setTimeout(() => setTextVisible(true), 600);
  }, []);

  return (
    <div
      className="min-h-screen flex items-center justify-center p-6"
      style={{ background: 'linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #3d2010 100%)' }}
    >
      <div
        className="w-full max-w-md transition-all duration-700"
        style={{ opacity: visible ? 1 : 0, transform: visible ? 'translateY(0)' : 'translateY(30px)' }}
      >
        <div
          className="rounded-3xl overflow-hidden shadow-2xl"
          style={{ background: '#f8f4ef', border: '1px solid #e0d6c8' }}
        >
          {/* Coffee image with overlay */}
          <div
            className="relative w-full transition-all duration-700"
            style={{ height: '260px', opacity: imgVisible ? 1 : 0, transform: imgVisible ? 'scale(1)' : 'scale(1.05)' }}
          >
            <Image
              src={personality.image}
              alt={personality.coffee}
              fill
              className="object-cover"
            />
            <div
              className="absolute inset-0"
              style={{ background: 'linear-gradient(to bottom, transparent 50%, #f8f4ef 100%)' }}
            />
          </div>

          {/* Content */}
          <div
            className="px-10 pb-10 text-center transition-all duration-700"
            style={{ opacity: textVisible ? 1 : 0, transform: textVisible ? 'translateY(0)' : 'translateY(16px)' }}
          >
            <p
              className="text-xs font-semibold mb-4 tracking-widest uppercase"
              style={{ color: '#b0a090', fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', letterSpacing: '3px' }}
            >
              Твой тип
            </p>

            <h2
              className="text-3xl font-bold mb-3 tracking-tight"
              style={{ fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', color: '#1a0f08', lineHeight: '1.2' }}
            >
              {personality.name}
            </h2>

            <div style={{ width: '40px', height: '2px', background: '#c4a882', margin: '16px auto' }} />

            <div
              className="inline-flex items-center gap-2 px-5 py-2 rounded-full mb-5"
              style={{ background: '#1a0f08', color: '#f8f4ef' }}
            >
              <span style={{ fontSize: '14px', fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', letterSpacing: '0.5px' }}>
                ☕ {personality.coffee}
              </span>
            </div>

            <p
              className="text-base italic mb-8"
              style={{ color: '#7a6050', fontFamily: 'Georgia, serif', lineHeight: '1.6', fontSize: '17px' }}
            >
              «{personality.tagline}»
            </p>

            <p
              className="text-sm mb-6"
              style={{ color: '#a09080', fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', lineHeight: '1.6' }}
            >
              Приходи в кофейню и назови свой тип — бариста знает, что приготовить!
            </p>

            <button
              onClick={onRestart}
              className="w-full py-4 rounded-2xl text-sm font-semibold transition-all duration-300"
              style={{
                background: 'transparent',
                color: '#6b5848',
                border: '1.5px solid #d4c4b0',
                fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif',
                letterSpacing: '0.5px',
              }}
              onMouseEnter={(e) => { e.currentTarget.style.background = '#f0e8dc'; e.currentTarget.style.borderColor = '#c4a882'; }}
              onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.borderColor = '#d4c4b0'; }}
            >
              Пройти ещё раз
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
