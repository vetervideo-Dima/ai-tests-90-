'use client';

import { useState, useMemo } from 'react';
import { questions, personalities, PersonalityKey } from '@/app/data/quiz';
import QuizStart from '@/app/components/QuizStart';
import QuizQuestion from '@/app/components/QuizQuestion';
import QuizResult from '@/app/components/QuizResult';

type QuizState = 'start' | 'question' | 'result';

export default function Home() {
  const [state, setState] = useState<QuizState>('start');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [scores, setScores] = useState<Record<PersonalityKey, number>>({
    adventurer: 0,
    classic: 0,
    sweet: 0,
    zen: 0,
    social: 0,
    owl: 0,
  });

  const resultPersonality = useMemo(() => {
    const maxKey = Object.keys(scores).reduce((a, b) =>
      scores[a as PersonalityKey] > scores[b as PersonalityKey] ? a : b
    ) as PersonalityKey;
    return personalities[maxKey];
  }, [scores]);

  const handleStart = () => {
    setState('question');
    setCurrentQuestion(0);
    setScores({
      adventurer: 0,
      classic: 0,
      sweet: 0,
      zen: 0,
      social: 0,
      owl: 0,
    });
  };

  const handleAnswer = (personality: PersonalityKey) => {
    setScores((prev) => ({
      ...prev,
      [personality]: prev[personality] + 1,
    }));

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
    } else {
      setState('result');
    }
  };

  const handleRestart = () => {
    setState('start');
  };

  return (
    <main className="min-h-screen" style={{ background: 'linear-gradient(135deg, #2c1810 0%, #4a2c1a 50%, #3d2010 100%)' }}>
      {state === 'start' && <QuizStart onStart={handleStart} />}
      {state === 'question' && (
        <QuizQuestion
          question={questions[currentQuestion]}
          currentQuestion={currentQuestion + 1}
          totalQuestions={questions.length}
          onAnswer={handleAnswer}
        />
      )}
      {state === 'result' && (
        <QuizResult personality={resultPersonality} onRestart={handleRestart} />
      )}
    </main>
  );
}
