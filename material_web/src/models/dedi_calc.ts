import { useState } from 'react';

import type { CalcDediType } from '@/types/calc.d';

export default function DediCalc() {
  const [calcType, setCalcType] = useState<CalcDediType>('dedi');
  const [calcRes, setCalcRes] = useState<any>();

  return {
    calcType,
    setCalcType,
    calcRes,
    setCalcRes,
  };
}
