'use client';
import { useEffect, useState } from 'react';
import { QuizQuestion as QuizQuestionType, QuizOption, PersonalityKey } from '@/app/data/quiz';

interface QuizQuestionProps {
  question: QuizQuestionType;
  currentQuestion: number;
  totalQuestions: number;
  onAnswer: (personality: PersonalityKey) => void;
}

export default function QuizQuestion({ question, currentQuestion, totalQuestions, onAnswer }: QuizQuestionProps) {
  const [visible, setVisible] = useState(false);
  const [selected, setSelected] = useState<number | null>(null);

  useEffect(() => {
    setVisible(false);
    setSelected(null);
    const t = setTimeout(() => setVisible(true), 80);
    return () => clearTimeout(t);
  }, [question.id]);

  const handleSelect = (personality: PersonalityKey, index: number) => {
    if (selected !== null) return;
    setSelected(index);
    setTimeout(() => onAnswer(personality), 400);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 py-10">
      <div
        className="w-full max-w-xl transition-all duration-500"
        style={{ opacity: visible ? 1 : 0, transform: visible ? 'translateY(0)' : 'translateY(20px)' }}
      >
        {/* Dot progress indicator */}
        <div className="flex items-center justify-center gap-2 mb-6">
          {Array.from({ length: totalQuestions }).map((_, i) => (
            <div
              key={i}
              className="transition-all duration-300"
              style={{
                width: i === currentQuestion - 1 ? '28px' : '10px',
                height: '10px',
                borderRadius: '5px',
                background: i < currentQuestion ? '#1a0f08' : 'rgba(248,244,239,0.35)',
                border: i === currentQuestion - 1 ? 'none' : i < currentQuestion ? 'none' : '1.5px solid rgba(248,244,239,0.5)',
              }}
            />
          ))}
        </div>

        {/* Question card */}
        <div
          className="rounded-3xl p-8 shadow-2xl"
          style={{ background: '#f8f4ef', border: '1px solid #e0d6c8' }}
        >
          <p
            className="text-xs font-semibold mb-3 tracking-widest uppercase text-center"
            style={{ color: '#b0a090', fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', letterSpacing: '2px' }}
          >
            Вопрос {currentQuestion} из {totalQuestions}
          </p>
          <h2
            className="text-xl font-bold mb-6 text-center"
            style={{ fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif', color: '#1a0f08', lineHeight: '1.4' }}
          >
            {question.text}
          </h2>

          <div className="flex flex-col gap-2">
            {question.options.map((option: QuizOption, index: number) => (
              <button
                key={index}
                onClick={() => handleSelect(option.personality, index)}
                className="p-4 text-left rounded-2xl transition-all duration-200"
                style={{
                  background: selected === index ? '#1a0f08' : '#fff',
                  border: `1.5px solid ${selected === index ? '#1a0f08' : '#e0d6c8'}`,
                  color: selected === index ? '#f8f4ef' : '#2c1810',
                  fontSize: '15px',
                  fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif',
                  transform: selected === index ? 'scale(1.02)' : 'scale(1)',
                  opacity: selected !== null && selected !== index ? 0.45 : 1,
                  cursor: selected !== null ? 'default' : 'pointer',
                }}
                onMouseEnter={(e) => {
                  if (selected !== null) return;
                  e.currentTarget.style.background = '#f0e8dc';
                  e.currentTarget.style.borderColor = '#c4a882';
                  e.currentTarget.style.transform = 'translateX(4px)';
                }}
                onMouseLeave={(e) => {
                  if (selected !== null) return;
                  e.currentTarget.style.background = '#fff';
                  e.currentTarget.style.borderColor = '#e0d6c8';
                  e.currentTarget.style.transform = 'translateX(0)';
                }}
              >
                <span className="text-xl mr-3">{option.emoji}</span>
                <span className="font-medium">{option.text}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
