import { message } from 'antd';

export const MsgGetSuccess = (typ: string, key: any) => {
  message.open({
    type: 'success',
    content: `${typ}: ${key} 获取成功！`,
  });
};

export const MsgGetError = (typ: string, key: any) => {
  message.open({
    type: 'error',
    content: `${typ}: ${key} 获取错误！`,
  });
};
