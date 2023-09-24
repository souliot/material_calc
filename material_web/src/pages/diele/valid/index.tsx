import { PageContainer, ProCard, ProForm, ProFormUploadButton } from '@ant-design/pro-components';
import { useIntl, useModel } from '@umijs/max';
import { Result } from 'antd';
import React from 'react';

import { εij } from '@/services/valid';

const Valid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { validItemStatus, setValidItemStatus, validItemDetail, setValidItemDetail } =
    useModel('valid');

  const OnValid = async (values: any) => {
    const data = new FormData();
    data.append('poscar', values.poscar[0].originFileObj);
    data.append('outcar_de', values.outcar_de[0].originFileObj);
    data.append('outcar_di', values.outcar_di[0].originFileObj);

    const res = await εij(data);

    if (res.code == 1) {
      setValidItemStatus('success');
      setValidItemDetail('');
      return;
    }
    setValidItemStatus('error');
    setValidItemDetail(res.message + '---' + res.data);
  };

  return (
    <PageContainer
      header={{
        breadcrumb: {},
      }}
    >
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
        <ProFormUploadButton
          name="outcar_de"
          label="OUTCAR_ele"
          title="请选择OUTCAR_ele文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR_ele文件!' }]}
        />
        <ProFormUploadButton
          name="outcar_di"
          label="OUTCAR_ion"
          title="请选择OUTCAR_ion文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR_ion文件!' }]}
        />
      </ProForm>
      <ProCard title="验证结果" style={{ marginTop: 20 }} bordered headerBordered>
        <Result
          status={validItemStatus}
          title={validItemStatus == 'success' ? '验证成功' : '验证失败'}
          subTitle={validItemDetail}
        />
      </ProCard>
    </PageContainer>
  );
};

export default Valid;
