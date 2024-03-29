

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
1. Navegue até _"Exports"_ no painel esquerdo. Clique em _"CREATE EXPORT"_
1. Nomeie a exportação como _"ga_sessions_creation"_ por exemplo, mas você pode nomear como quiser
1. Em "Sink Service" escolha _"Cloud Pub/Sub"_ e, abaixo, escolha a opção _"Create new Cloud Pub/Sub topic"_
1. Insira o nome do tópico - por exemplo _"ga_sessions_creation"_
1. Para adicionar o filtro de consulta, clique na seta para baixo e selecione _"Convert to advanced filter"_
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

Após essa configuração toda vez que uma nova tabela do _"ga_sessions\_"_ for criada, um requisição do Pub/Sub será disparada, servindo de gatilho para uma Google Cloud Function(GCF) ,podendo ser utilizada para diversas finalidades como por exemplo:

* [Exportar dados para o GCS]();
* [Schendular uma query no BQ]();

## Licença

Apache Version 2.0

See [Licença](https://github.com/mixplick/ga-table-trigger/blob/master/LICENSE)
