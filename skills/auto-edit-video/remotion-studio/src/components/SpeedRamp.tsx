import React from 'react';

export const SpeedRamp: React.FC<{
  normalRate?: number;
  slowRate?: number;
  fastRate?: number;
  slowStartFrame?: number;
  slowDuration?: number;
  children: React.ReactNode;
}> = ({ children }) => {
  return (
    <div style={{ width: '100%', height: '100%' }}>
      {children}
    </div>
  );
};
