import { useState } from 'react';

export default function ElaStable() {
  const [calcRes, setCalcRes] = useState<any>();

  return {
    calcRes,
    setCalcRes,
  };
}
