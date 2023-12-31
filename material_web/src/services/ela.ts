// @ts-ignore
// @eslint-disable
import { request } from '@umijs/max';

import { BasicApiResponse } from '@/types/basic';

const BASIC_PATH = '/api/v1/ela';

export async function ela(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}

export async function hkl(data: any) {
  const res = await request(`${BASIC_PATH}/hkl`, {
    method: 'POST',
    data,
  });
  return res;
}

export async function img(data: any) {
  const res = await request(`${BASIC_PATH}/hkl/img`, {
    method: 'POST',
    data,
    responseType: 'blob',
  });
  return res;
}

export async function download(data: any) {
  const res = await request(`${BASIC_PATH}/hkl/download`, {
    method: 'POST',
    data,
    responseType: 'blob',
  });
  return res;
}
