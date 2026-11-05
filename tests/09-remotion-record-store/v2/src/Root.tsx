// src/Root.tsx
import React from 'react';
import {Composition} from 'remotion';
import {GrooveBasement} from './GrooveBasement';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="GrooveBasement"
      component={GrooveBasement}
      durationInFrames={450}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
