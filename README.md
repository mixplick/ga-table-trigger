<img src="https://www.dp6.com.br/wp-content/uploads/2017/12/logo-cor.png" alt="DP6 logo" title="DP6" align="right" height="50" width="160"/>

# [Bigquery GA Sessions: Table Created Trigger](https://github.com/mixplick/ga-table-trigger)

Quando temos uma conta de Google Analytics(GA) 360, existe a possibilidade de exportar esse dados para o Bigquery(BQ), ativando o [BigQuery Export para o Google Analytics](https://support.google.com/analytics/answer/3437618?hl=pt-BR&ref_topic=3416089), gerando diariamente uma tabela no BQ com os dados das sessões e hits. Muitas vezes precisamos fazer alguma ação após uma nova tabela é criada e esses dados estão disponíveis, atualizar a tabela de um dashboard ou exportar esses dados em CSV.

Neste documeto explicaremos em etapas como criar gatilhos que possa ser usado tanto para agendar uma query no BQ ou exportar um arquivo para o Google Cloud Storage(GCS).

**Índice:**

* [Permissões Necessárias](#permissões-necessárias)
* [Stackdrive](#criando-uma-exportação-do-stackdrive-para-o-pub/sub)
* [Licença](#licença)

## Permissões Necessárias

Para a criação dessa estrutura são necessárias alguma permissões de acesso no projeto do GCP, listadas abaixo:

* roles/editor;
* roles/cloudfunctions.admin;
* roles/bigquery.admin;
* roles/logging.admin;
* roles/storage.admin;

## Criando uma exportação do Stackdrive para o Pub/Sub

1. Vá para a seção Logging no menu lateral
1. Navegue até "Exports" no painel esquerdo. Clique em "CREATE EXPORT"
1. Nomeie a exportação como "ga_sessions_creation" por exemplo, mas você pode nomear como quiser
1. Em "Sink Service" escolha "Cloud Pub/Sub" e, abaixo, escolha a opção "Create new Cloud Pub/Sub topic"
1. Insira o nome do tópico - por exemplo "ga_sessions_creation"
1. Para adicionar o filtro de consulta, clique na seta para baixo e selecione "Convert to advanced filter"
1. Remova o texto na caixa de texto resultante e substitua-o por:

```bash
resource.type="bigquery_resource"
protoPayload.methodName="jobservice.jobcompleted"
protoPayload.serviceData.jobCompletedEvent.eventName="load_job_completed"
protoPayload.authenticationInfo.principalEmail="analytics-processing-dev@system.gserviceaccount.com"
protoPayload.serviceData.jobCompletedEvent.job.jobConfiguration.load.destinationTable.tableId:"ga_sessions_"
protoPayload.serviceData.jobCompletedEvent.job.jobConfiguration.load.destinationTable.datasetId:"<datasetid>"
NOT
protoPayload.serviceData.jobCompletedEvent.job.jobConfiguration.load.destinationTable.tableId:"ga_sessions_intraday"
```

Agora toda vez que uma nova tabela do ga_sessions_* for criada, um requisição do Pub/Sub será disparada.

## Licença

Apache Version 2.0

See [Licença](https://github.com/mixplick/ga-table-trigger/blob/master/LICENSE)
