import { useState } from 'react';

export default function DijCalc() {
  const [calcRes, setCalcRes] = useState<any>();

  return {
    calcRes,
    setCalcRes,
  };
}
