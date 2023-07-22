import { useState } from 'react';

import type { ValidStatus } from '@/types/valid.d';

export default function Valid() {
  const [validAllStatus, setAllValidStatus] = useState<ValidStatus>('success');
  const [validItemStatus, setValidItemStatus] = useState<ValidStatus>('success');
  const [validAllDetail, setValidAllDetail] = useState<string>();
  const [validItemDetail, setValidItemDetail] = useState<string>();

  return {
    validAllStatus,
    setAllValidStatus,
    validItemStatus,
    setValidItemStatus,
    validAllDetail,
    setValidAllDetail,
    validItemDetail,
    setValidItemDetail,
  };
}
