import { useState } from 'react';

export default function ElaCalc() {
  const [hklLoading, setHklLoading] = useState<boolean>(false);
  const [calcRes, setCalcRes] = useState<any>();

  return {
    hklLoading,
    setHklLoading,
    calcRes,
    setCalcRes,
  };
}
