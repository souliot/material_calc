import { useState } from 'react';

export default function DediCalc() {
  const [calcRes, setCalcRes] = useState<any>();

  return {
    calcRes,
    setCalcRes,
  };
}
