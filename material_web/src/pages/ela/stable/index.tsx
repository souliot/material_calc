import {
  PageContainer,
  ProCard,
  ProDescriptions,
  ProForm,
  ProFormUploadButton,
} from '@ant-design/pro-components';
import { useIntl, useModel } from '@umijs/max';
import { Button } from 'antd';
import React from 'react';

import { ela } from '@/services/ela';

const ElaStable: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { calcRes, setCalcRes } = useModel('ela_stable');
  const { dataForm } = useModel('ela');

  const resColumns = [
    {
      title: '稳定性结论',
      key: 'stable',
      dataIndex: 'stable',
      valueType: 'code',
      copyable: true,
    },
  ];

  const onCalcEla = async (values: any) => {
    setCalcRes({});
    const data = new FormData();
    data.append('poscar', values.poscar[0].originFileObj);
    data.append('outcar', values.outcar[0].originFileObj);

    const res = await ela(data);
    if (res.code != 1) {
      return;
    }
    setCalcRes(res.data);
  };

  return (
    <PageContainer
      header={{
        breadcrumb: {},
      }}
    >
      <ProForm
        submitter={{
          searchConfig: {
            submitText: intl.formatMessage({
              id: 'pages.ela.stable',
              defaultMessage: 'Material Calc',
            }),
          },
          render: ({ form }, doms) => {
            return [...doms];
          },
        }}
        form={dataForm}
        onFinish={async (values) => {
          await onCalcEla(values);
        }}
      >
        <ProFormUploadButton
          name="poscar"
          label="POSCAR"
          title="请选择POSCAR文件"
          extra="目前支持POSCAR文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择POSCAR文件!' }]}
        />
        <ProFormUploadButton
          name="outcar"
          label="OUTCAR"
          title="请选择OUTCAR文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR文件!' }]}
        />
      </ProForm>
      <ProCard
        title="计算结果"
        subTitle=""
        style={{ marginTop: 20 }}
        bordered
        headerBordered
        extra={
          <Button
            onClick={async () => {
              await setCalcRes({});
            }}
            key="refresh"
          >
            重置
          </Button>
        }
      >
        <ProDescriptions column={1} size={'middle'} dataSource={calcRes} columns={resColumns} />
      </ProCard>
    </PageContainer>
  );
};

export default ElaStable;
