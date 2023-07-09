import {
  FooterToolbar,
  PageContainer,
  ProForm,
  ProFormTextArea,
  ProFormUploadDragger,
} from '@ant-design/pro-components';
import { useIntl } from '@umijs/max';
import React from 'react';

const ElaValid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const OnValid = (values: any) => {
    console.log(values);
  };

  return (
    <PageContainer title={' '}>
      <ProForm
        submitter={{
          render: (_, dom) => <FooterToolbar>{dom}</FooterToolbar>,
        }}
        onFinish={async (values) => OnValid(values)}
      >
        <ProFormUploadDragger
          description="目前支持POSCAR文件"
          label="POSCAR"
          name="poscar"
          title="请选择POSCAR文件"
          rules={[{ required: true, message: '请选择POSCAR文件!' }]}
        />
        <ProFormTextArea
          name="mat"
          label="Cij 矩阵"
          placeholder="请输入Cij矩阵"
          rules={[{ required: true, message: '请输入Cij矩阵' }]}
          fieldProps={{
            autoSize: { minRows: 12, maxRows: 20 },
          }}
        />
      </ProForm>
    </PageContainer>
  );
};

export default ElaValid;
