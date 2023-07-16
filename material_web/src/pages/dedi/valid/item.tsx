import { ProCard, ProForm, ProFormTextArea, ProFormUploadButton } from '@ant-design/pro-components';
import { useIntl, useModel } from '@umijs/max';
import { Result } from 'antd';
import React from 'react';

import { piezo } from '@/services/valid';

const ItemValid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { validItemStatus, setValidItemStatus, validItemDetail, setValidItemDetail } =
    useModel('valid');

  const OnValid = async (values: any) => {
    const data = new FormData();
    data.append('mat', values.mat);
    data.append('poscar', values.poscar[0].originFileObj);

    const res = await piezo(data);

    if (res.code == 1) {
      setValidItemStatus('success');
      return;
    }
    setValidItemStatus('error');
    setValidItemDetail(res.data);
  };

  return (
    <>
      <ProForm
        submitter={{
          render: (props, doms) => {
            return [...doms];
          },
        }}
        onFinish={async (values) => {
          await OnValid(values);
          return true;
        }}
      >
        <ProFormUploadButton
          extra="目前支持POSCAR文件"
          label="POSCAR"
          name="poscar"
          title="请选择POSCAR文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择POSCAR文件！' }]}
        />
        <ProFormTextArea
          name="mat"
          label="Piezo 矩阵"
          placeholder="请输入Piezo矩阵"
          tooltip="3*6 矩阵，空格分割"
          rules={[{ required: true, message: '请输入Piezo矩阵！' }]}
          fieldProps={{
            autoSize: { minRows: 11, maxRows: 20 },
          }}
        />
      </ProForm>
      <ProCard title="验证结果" style={{ marginTop: 20 }} bordered headerBordered>
        <Result
          status={validItemStatus}
          title={validItemStatus == 'success' ? '验证成功' : '验证失败'}
          subTitle={validItemDetail}
        />
      </ProCard>
    </>
  );
};

export default ItemValid;
