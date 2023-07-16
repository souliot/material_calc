import { PageContainer } from '@ant-design/pro-components';
import { useIntl, useModel } from '@umijs/max';
import React from 'react';

import type { ValidType } from '@/types/valid.d';
import AllValid from './all';
import ItemValid from './item';

const ElaValid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { validType, setValidType } = useModel('valid');

  const tabList = [
    {
      tab: intl.formatMessage({
        id: 'pages.ela.valid.matrix',
        defaultMessage: 'Material Calc',
      }),
      key: 'cij',
      children: <ItemValid />,
    },
    {
      tab: '全部',
      key: 'all',
      children: <AllValid />,
    },
  ];

  const onTabChange = async (key: string) => {
    setValidType(key as ValidType);
  };
  return (
    <PageContainer
      header={{
        title: '',
        breadcrumb: {},
      }}
      tabActiveKey={validType}
      tabList={tabList}
      onTabChange={(key) => {
        onTabChange(key);
      }}
    ></PageContainer>
  );
};

export default ElaValid;
