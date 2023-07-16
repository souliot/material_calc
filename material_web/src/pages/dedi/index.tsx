import { PageContainer } from '@ant-design/pro-components';
import { useIntl } from '@umijs/max';
import React from 'react';

const ElaValid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  return (
    <PageContainer
      header={{
        title: '',
        breadcrumb: {},
      }}
    >
      Hello
    </PageContainer>
  );
};

export default ElaValid;
