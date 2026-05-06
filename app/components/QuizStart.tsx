'use client';
import { useEffect, useState } from 'react';

interface QuizStartProps {
  onStart: () => void;
}

export default function QuizStart({ onStart }: QuizStartProps) {
  const [visible, setVisible] = useState(false);
  useEffect(() => { setTimeout(() => setVisible(true), 50); }, []);

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div
        className="w-full max-w-lg text-center transition-all duration-700"
        style={{ opacity: visible ? 1 : 0, transform: visible ? 'translateY(0)' : 'translateY(24px)' }}
      >
        <div
          className="rounded-3xl p-12 shadow-2xl"
          style={{ background: '#f8f4ef', border: '1px solid #e0d6c8' }}
        >
          <div className="text-6xl mb-6">☕</div>
          <h1
            className="text-4xl font-bold mb-3 tracking-tight"
            style={{ fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', color: '#1a0f08' }}
          >
            Кофейный тест
          </h1>
          <p
            className="text-base mb-2 font-medium tracking-widest uppercase"
            style={{ fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', color: '#8a7060', letterSpacing: '3px', fontSize: '11px' }}
          >
            Вайб Кофе
          </p>
          <div style={{ width: '40px', height: '2px', background: '#c4a882', margin: '20px auto 24px' }} />
          <p style={{ color: '#6b5848', lineHeight: '1.8', fontSize: '16px', fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif' }}>
            Ответь на 6 вопросов и узнай,<br />какой кофе создан именно для тебя.
          </p>

          <button
            onClick={onStart}
            className="mt-10 w-full py-5 px-8 text-base font-semibold rounded-2xl transition-all duration-300"
            style={{
              fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif',
              background: '#1a0f08',
              color: '#f8f4ef',
              border: 'none',
              letterSpacing: '0.5px',
              fontSize: '15px',
            }}
            onMouseEnter={(e) => { e.currentTarget.style.background = '#3d2010'; e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 8px 24px rgba(26,15,8,0.3)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.background = '#1a0f08'; e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}
          >
            Начать тест →
          </button>

          <p className="text-sm mt-5" style={{ color: '#b0a090', fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif' }}>
            6 вопросов · 2 минуты
          </p>
        </div>
      </div>
    </div>
  );
}
