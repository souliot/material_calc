import { useState } from 'react';

import type { ValidStatus, ValidType } from '@/types/valid.d';

export default function Valid() {
  const [validAllStatus, setAllValidStatus] = useState<ValidStatus>('success');
  const [validItemStatus, setValidItemStatus] = useState<ValidStatus>('success');
  const [validAllDetail, setValidAllDetail] = useState<string>();
  const [validItemDetail, setValidItemDetail] = useState<string>();
  const [validType, setValidType] = useState<ValidType>();

  return {
    validAllStatus,
    setAllValidStatus,
    validItemStatus,
    setValidItemStatus,
    validAllDetail,
    setValidAllDetail,
    validItemDetail,
    setValidItemDetail,
    validType,
    setValidType,
  };
}
