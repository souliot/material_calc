import { useState } from 'react';

export default function ElaCalc() {
  const [calcRes, setCalcRes] = useState<any>();

  return {
    calcRes,
    setCalcRes,
  };
}
