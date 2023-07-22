import { useState } from 'react';

export default function DieleCalc() {
  const [calcRes, setCalcRes] = useState<any>();

  return {
    calcRes,
    setCalcRes,
  };
}
