import React from 'react';
import {Composition} from 'remotion';
import {MyComposition} from './MyComposition';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={240}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
