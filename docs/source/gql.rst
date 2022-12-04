GraphQL documentation
=====================

**Q.Platform**
================

**Queries**
------------

AhAttribute
^^^^^^^^^^^^

   This query fetches the type of attribute for entity template used. The model stores the details of the attributes that are associated with any given entity template.
The available attribtues of this query are as follows:
******************************************************

-  **id**: The ID of the attribute
-  **name** : The name of the attribute whose value is to be returned.
-  **is_required**: Whether the attribute value will be required for the entity instance that will be created with the associated entity template
-  **entity_template**: The entity template with which this attribute will be associated with 
.. (add hyperlink here)
-  **attribute_type**:of measurement for the given attribute
-  **is_array**: Whether the attribute value would be an array
-  **data_type**: The data type of the attribute when its value will be stored in AhEntityAttributeValue table
-  **description**: The description or information about the fetched attribute.
-  **createdAt**: The created at time of the attribute in epoch
-  **updatedAt**: The updated at time of the attribute in epoch
-  **attribtueValues**: All the values for attribute
-  **aliasTag**: Get alias tag for the attribute

.. list-table:: Types of attributes
   :widths: 50
   :header-rows: 1

   * - Type
   * - PROCESS_UNIT_HIERARCHY
   * - RECOMMENDED_ATTRIBUTE
   * - CUSTOM_ATTRIBUTE
   * - ALIAS_TAG
   * - WORK_CELL_HIERARCHY

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-  **entityTemplate**: Filter on the basis of entity template used.
-  **id**: For a particular ID.
-  **limit**: Number of results to return per page. Default 'default_limit': None, and 'max_limit': None
-  **name_Icontains**: If name contains the given string
-  **name_Iexact**: If exact name match the string
-  **ordering**: Order results by the attribute
-  **offset**: The initial index from which to return the results. Default: 0


AhEntity
^^^^^^^^^^^^

  This query fetches the type of attribute for entity template used. 
  The model stores the details of the attributes that are associated with any given entity template.
The available attribtues of this query are as follows:
*******************************************************
- **attributeValues**: Values of the attributes of that entity
- **asset**: Asset to which the entity belongs to
- **createdAt**: The created at time of the attribute in epoch
- **id**: ID of the
- **name**: Name of the entity
- **totalAssetTags**:
- **site**: Get required site details
- **totalAssets**: Total count of the assets
- **updatedAt**: The updated at time of the attribute in epoch
- **entityTemplate**: Template to which the entity belongs to


The available paramters to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **entityTemplate**: Filter by template ID
- **entityTemplate_Name_Icontains**: If name contains the string
- **entityTemplate_Name_Iexact**: If name matches the string
- **id**: Filter by ID
- **limit**: Number of results to return per page. Default 'default_limit': None, and 'max_limit': None
- **name_Icontains**: If name contains the given string
- **name_Iexact**: If exact name match the string
- **offset**: The initial index from which to return the results. Default: 0
- **ordering**: Order results by the attribute


AhEntityAttributeValue
^^^^^^^^^^^^^^^^^^^^^^^

   This query gives all values for an attribute pertaining to the entities.
The available attribtues of this query are as follows:
*************************************

-  **assetEntityCount**: Refers to the the count of asset entities present in the given process unit or work cell entity template.
-  **attribute**: Refers to the attribute whose value is being refered to
-  **createdAt**: The created at time of the attribute in epoch
-  **entity**: Refers to the entity, whose attribute value is to be stored
-  **id**: ID of the EntityAttributeValue
-  **updatedAt**: The updated at time of the attribute in epoch
-  **value**: Refers to the value that is stored as string


The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **attribtue**: Filter by attribute
- **entity**: Filter by entity
- **id**: Filter by ID 
- **limit**: Number of results to return per page. Default 'default_limit': None, and 'max_limit': None
- **offset**: The initial index from which to return the results. Default: 0
- **ordering**: Order results by the attribute


AhEntityTemplate
^^^^^^^^^^^^^^^^^

   This query is used to fetch all the templates present for the given entity type.
The available attribtues of this query are as follows:
******************************************************

-  **AhAttributes**: List of attributes
-  **id**: The ID of the Entity template
-  **name** : The name of the Entity template whose value is to be returned.
-  **is_required**: Whether the Entity template value will be required for the entity instance that will be created with the associated entity template
-  **entity_template**: The entity template with which this attribute will be associated with 
-  **entity_type**: The entity type with which this attribute will be associated with 
.. (add hyperlink here)
-  **createdAt**: The created at time of the attribute in epoch
-  **updatedAt**: The updated at time of the attribute in epoch
-  **hierarchy**: Get Ahattribute objects which are of type PROCESS_UNIT_HIERARCHY or WORK_CELL_HIERARCHY
-  **sites**: Get required site details

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **entityType**: Filter by entity type
- **id**: Filer by ID 
- **limit**: Number of results to return per page. Default 'default_limit': None, and 'max_limit': None
- **name_Icontains**: If name contains the given string
- **name_Iexact**: If exact name match the string
- **offset**: The initial index from which to return the results.
- **ordering**: Order results by the attribute.


AhEntityType
^^^^^^^^^^^^^

 This query gives the entity type and related information.
The available attribtues of this query are as follows:
*******************************************************

-  **id**: ID of the Entity type
-  **name** : The name of the entity type whose value is to be returned.
-  **recommendedAttributes**: Recommended attributes for the type
-  **entity_templates**: The entity template with which this attribute will be associated with 
.. (add hyperlink here)
-  **createdAt**: The created at time of the attribute in epoch
-  **updatedAt**: The updated at time of the attribute in epoch


.. list-table:: Types of Entities
   :widths: 50
   :header-rows: 1

   * - Type
   * - Process Unit
   * - Work Cell
   * - Asset Class

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID 
- **limit**: Number of results to return per page. Default 'default_limit': None, and 'max_limit': None
- **offset**: The initial index from which to return the results. Default: 0
- **ordering**: Order results by the attribute.

Asset
^^^^^^^^^^^^^

This query  refers to the asset entity which contains the details of the asset. Asset contains all the properties of the base entity defined. The available attribtues of this query are as follows:

The available attribtues of this query are as follows:
*******************************************************

-  **id**: ID of the asset
-  **name** : The name of the attribute whose value is to be returned.
-  **recommendedAttributes**: ---
-  **canAddRuleDefinition**: The entity template with which this attribute will be associated with 
-  **canAddTags**: Tags addition boolean
-  **config**: Defines the configuration attributes
-  **edgeConnectors**: List of edgeConnectors for an asset
-  **entity**: one to one entity relation
-  **lastOverhaulDate**: DateTime of last maintenance of the asset
-  **lastStreamedOn**: DateTime of either of the tags streaming for the asset
-  **onboardedAt**: onboarding Datetime
-  **status**: Ehether the asset is running
-  **tags**: List of sensors assigned to the asset.


The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filer by ID
- **assetOperation**: filter by asset operation
- **entity**: filter by entity
- **name__Icontains**: if name contains the string
- **name__Iexact**: Exact name match the string
- **puWcId**: Process Unit/ Work cell, to which this asset is supposed to belong to
- **limit**: Number of results to return per page. Default 'default_limit': None, and 'max_limit': None
- **offset**: The initial index from which to return the results. Default: 0
- **ordering**: Order results by the attribute.


AssetComponent
^^^^^^^^^^^^^

This query fetches the information regarding the various components which comprises an asset.

The available attribtues of this query are as follows:
*******************************************************

-  **id**: ID of the The ID of the attribute
-  **asset** : Name of the asset to which the component belongs to.
-  **assetPermission**: Permissions pertaining to the component
-  **assetcomponentSet**: Set of other components in the order
-  **name** : The name of the attribute whose value is to be returned.
-  **parent**: parent of the component
-  **tags**: List of sensors assigned to the asset component.
.. (add hyperlink here)
-  **createdAt**: The created at time of the attribute in epoch
-  **updatedAt**: The updated at time of the attribute in epoch

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **asset**: Filter by asset
- **id**: Filter by ID
- **limit**: Number of results to return per page. Default 'default_limit': None, and 'max_limit': None
- **offset**: The initial index from which to return the results. Default: 0
- **ordering**: Order results by the attribute.


AssetOperation
^^^^^^^^^^^^^

This query tells if the asset is of batch or continous type. It has one to one relation with Asset.

The available attribtues of this query are as follows:
*******************************************************

-  **id**: ID of the The ID of the attribute
-  **asset** : Name of the asset to which the component belongs to.
-  **assetPermission**: Permissions pertaining to the component
-  **assetStateIdentifier**: Tag type attribute
-  **assetStopValue**: Value where the asset operation was stopped
-  **batchTag**: The batch which is currently running
-  **cyclePhaseTag**: Phase of the cycle for the asset.
-  **cycleTag**: Name of the current cycle tag
-  **operationType**: Batch or Continuous asset
-  **osiBatchIdAttr**: --
-  **startState**: Tag from which the operation is started.
-  **stopState**: Tag from which the operation is ended.
-  **createdAt**: The created at time of the attribute in epoch
-  **updatedAt**: The updated at time of the attribute in epoch
-  **alarmTags**: List of flags raised

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **asset**: Filter by asset
- **createdAt**: The created at time of the attribute in epoch
- **createdAt_Gt**: Greater than created at datetime
- **createdAt_Gte**: Greater than or equal to created at datetime
- **createdAt_Lt**: Less than created at datetime
- **createdAt_Lte**: Less than or equal to created at datetime
- **id**: Filter by ID 
- **limit**: Limit the number of objects in query
- **offset**: Offset objects by number
- **operationType**:
- **ordering**:
- **updatedAt**: The updated at time of the attribute in epoch 
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte**: less than or equal to updated at datetime



ManualProcedureBatch
^^^^^^^^^^^^^^^^^^^^^

   
The available attribtues of this query are as follows:
*******************************************************

- **batchName**: name of the batch
- **createdAt**: created at date time
- **id**: id of the batch
- **procedure**: procedure used
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **batchName_Icontains**: 
- **batchName_Iexact**:
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **procedure_Id**: filter by procedure id


Product
^^^^^^^^^^^^^

This query gives the product related fields' information.

The available attribtues of this query are as follows:
*******************************************************
- **createdAt**: created at datetime
- **description**: description of the product
- **id**: ID of the product
- **name**: name of the product
- **productProcedures**: List of procedures
- **ruleDefinitions**: list of rule definitions
- **totalBatchCount**: count of the total batch
- **updatedAt**: updated at datetime

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **name__Icontains**: if name contains the string
- **name__Iexact**: Exact name match the string
- **ordering**: Order results by the attribute



checkEdgeRequestResult
^^^^^^^^^^^^^^^^^^^^^^^


The available attribtues of this query are as follows:
*******************************************************


The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

csvUploadStatus
^^^^^^^^^^^^^^^

   

The available attribtues of this query are as follows:
*******************************************************


The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

deviceRequests
^^^^^^^^^^^^^^^

   description comes here

The available attribtues of this query are as follows:
*******************************************************


The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

deviceConfigs
^^^^^^^^^^^^^^^

   description comes here

The available attribtues of this query are as follows:
*******************************************************


The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



 
**Mutations**
----------------

AhattributeCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahattribute**: created attribute

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newAhattribute**: Values of different members of the object


AhattributeDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahattribute**: deleted attribute 

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the attribute to be deleted

AhattributeUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahattribute**: Updated attribtue

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateAhattribute**: values of different members of the object


AhentityCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahattribute**: created Ahentity

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newAhentity**: Values of different members of the object


AhattributeDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahAhentity**: deleted Ahentity

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Ahentity to be deleted

AhentityUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahentity**: Updated Ahentity

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateAhentity**: values of different members of the object


AhentityattributevalueCreate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahentityattribute**:

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newAhentity** :values of different members of the object 

AhentityattributevalueDelete
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahentityattribute**: deleted

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID to be deleted

AhentityattributevalueUpdate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahentityattribute**: updated

The available paramter to filter this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateAhentityattributevalue**: values of different members of the object 


AhentitytemplateCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ahentitytemplate**: created Ahentitytemplate

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newAhentitytemplate**: Values of different members of the object


AhentitytemplateDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Ahentitytemplate**: deleted Ahentitytemplate

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Ahentitytemplate to be deleted

AhentitytemplateUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Ahentitytemplate**: Updated Ahentitytemplate

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateAhentitytemplate**: Values of different members of the object


AssetCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Asset**: created Asset

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newAsset**: Values of different members of the object


AssetDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Asset**: deleted Asset

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Asset to be deleted

AssetUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Asset**: Updated Asset

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateAsset**: Values of different members of the object



AssetOperationCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **AssetOperation**: created AssetOperation

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newAssetOperation**: Values of different members of the object


AssetOperationDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **AssetOperation**: deleted AssetOperation

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the AssetOperation to be deleted

AssetOperationUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **AssetOperation**: Updated AssetOperation

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateAssetOperation**: Values of different members of the object




AssetcomponentCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Assetcomponent**: created Assetcomponent

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newAssetcomponent**: Values of different members of the object


AssetcomponentDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Assetcomponent**: deleted Assetcomponent

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Assetcomponent to be deleted

AssetcomponentUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Assetcomponent**: Updated Assetcomponent

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateAssetcomponent**: Values of different members of the object


DuplicateProcedureUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Procedure**: Updated Procedure

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateProcedure**: Values of different members of the object


ManualprocedurebatchCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Manualprocedurebatch**: created Manualprocedurebatch

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newManualprocedurebatch**: Values of different members of the object


ManualprocedurebatchDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Manualprocedurebatch**: deleted Manualprocedurebatch

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Manualprocedurebatch to be deleted

ManualprocedurebatchUpdate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Manualprocedurebatch**: Updated Manualprocedurebatch

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateManualprocedurebatch**: Values of different members of the object


ProductCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **product**: created product

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newproduct**: Values of different members of the object


ProductDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **product**: deleted product

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the product to be deleted

ProductUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **product**: Updated product

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateProduct**: Values of different members of the object




**Q.Data/Qnnect**
===================

**Queries**
----------------

Country
^^^^^^^^^^^^^
This query gives the country informationof the Site.

The available attribtues of this query are as follows:
*******************************************************

- **country**: site country
- **createdAt**: created DateTime
- **id**: Country ID
- **isoCode**: ISO Code 
- **name**: Name of the country
- **states**: states of the country
- **updatedAt**: updated at datetime

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID 
- **limit**: Limit the number of objects in query
- **offset**: Offset objects by number
- **ordering**:


EdgeConnector
^^^^^^^^^^^^^^^
This query refers to the datasource entity which contains the details of the datasource.

The available attribtues of this query are as follows:
*********************************************************

- **assetSet**: Tells connector's Tags belongs to which asset
- **assignedTagsCount**: Count of assigned tags to an asset
- **auditStorageRetentionDurationInMs**: Data stored period for short term
- **coldStorageRetentionDurationInMs**: Long term data access duration
- **config**: Configuration attributes
- **connectorProtocol**: protocol defining the Type of data incoming
- **containsTagUsedInAssetOpDef**: Whether it has tags defined in asset operation
- **createdAt**: created at datetime
- **edgeDevice**: edge device pertaining to this connector
- **etlSheets**: Sheets uploaded for auto-creation of tags
- **hotStorageRetentionDurationInMs**: Regular accessed data(9 months)
- **id**: ID of the Connector
- **lastStreamedOn**: last stream datetime 
- **name**: name of the connector
- **parent**: parent of the connector(applicable only for SQL)
- **rawTagsCount**: count of the raw tags assigned
- **ruleDefinitions**: rules written for the tag on the connector
- **streamStatus**: stream status 
- **streamingTagsCount**: count of streaming tags
- **subEdgeConnectors**: Edge connectors 
- **tagCapacity**: Tag count threshold
- **tags**: List of tags associate
- **totalTagsCount**: Count of the tags
- **unassignedTagsCount**: Count of the tags not assigned
- **updateInterval**:--
- **updatedAt**: updated at datetime
- **userEmailForAlerts**: List of emails of the user for alerts
- **userPhoneNumberForAlerts**: List of phone numbers of the users for sending alerts


The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **connectorProtocol**: filter by connector protocol (single value)
- **connectorProtocol_In**: filter by connector protocols (multi value)
- **edgeDevice**: Filter by edge Device.
- **edgeDevice_Name_Icontains**:  if device name contains the string
- **edgeDevice_Name_Iexact**: exact device name matches the string
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **name__Icontains**: if name contains the string
- **name__Iexact**: Exact name match the string
- **offset**: Offset objects by number
- **parent_EdgeDevice**: filter by parent edge device
- **ordering**: Order results by the attribute
- **updatedAt**: updated at date time
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte:** less than or equal to updated at datetime

EdgeNode
^^^^^^^^^^^^^

This query refers the information related to each Edge Node/ Edge Device.

The available attribtues of this query are as follows:
*******************************************************

- **childDevices**: list of the children edge nodes of the edge node
- **childDevicesCount**: Number of child edge nodes
- **config**: configuration attributes
- **containsTagUsedInAssetOpDef**: whether the node contains a tag to signify the batch
- **createdAt**: created at datetime
- **datasourcesCount**: count of the data sources
- **deployedModelsCount**: count of the deployed ML models
- **deviceBuild**: installer that gets created for the edge node
- **deviceType**: type of the device
- **edgeConnectors**: Data sources (one to many)
- **edgeLimitVals**: Limit threshold values of the node
- **heartBeatUpdate**: Tells whether the edge node is connected or not
- **id**: ID of the node
- **ipAddress**: IP address of the node
- **isConnected**: Boolean
- **lastStreamedOn**: Datetime of last stream
- **mlNodes**: Info. of all the assigned edge nodes for ML applications.
- **name**: Name of the Edge Node
- **os**: operating system
- **parent**: Parent of this Edge Node in the hierarchy
- **site**: SIte info. of the Node
- **systemStatus**: Info of the system status
- **totalTagsCount**: Count of the total tags
- **updatedAt**: updated at datetime

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **deviceType**: device type filter
- **error**: filter by error
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **name__Icontains**: if name contains the string
- **name__Iexact**: Exact name match the string
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **skipChildQlites**: boolean to filter one branch of child tree
- **status**: filter by status of the edge node


Site
^^^^^^^^^^^^^

This query gives all the information related to a Site. 

The available attribtues of this query are as follows:
*******************************************************
- **addressLine1**: address line 1 of the site
- **addressLine2**: address line 2 of the site
- **ahEntities**: ahEntities belonging to the site
- **country**: country of the site
- **createdAt**: created at datetime
- **customAttributes**: array of data_type, label_name, value and measurement unit.
- **edgeDevices**: List of edge devices
- **id**: ID of the site
- **name**: name of the site
- **pinCode**: pincode of the area of the site
- **processUnits**: List of process units
- **siteProcedures**: (many to many) 
- **state**: state of the city of the site
- **totalAssets**: Total assests of the site
- **updatedAt**: updated at datetime
- **workCells**: workcells pertaining to process units

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **name__Icontains**: if name contains the string
- **name__Iexact**: Exact name match the string
- **ordering**: Order results by the attribute


State
^^^^^^^^^^^^^

This query gives the information about the geographical state of the Site.

The available attribtues of this query are as follows:
*******************************************************
- **city**: city of the state of the site
- **country**: country to which the state belongs
- **createdAt**: created at datetime
- **id**: ID of the state.
- **name**: name of the state
- **name2**: another name of the state
- **updatedAt**: updated at datetime

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **countryID**: Filter by country ID
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute



Tag
^^^^^^^^^^^^^


The available attribtues of this query are as follows:
*******************************************************
- **active**: boolean
- **alarmTags**:
- **alias** Attribute: alias attribute
- **asset**: asset to which it belongsd to
- **assetPermission**: permission it has
- **assetStateIdentifier**: operation under which tag is specified
- **assetcomponentSet**: components to which it refers to
- **batchTags**: referes to asset op .definition
- **category**: intelligence category
- **childTags**: children tag
- **config**: configuration
- **createdAt**: created at date time 
- **cyclePhaseTag**: 
- **cycleTags**:
- **description**: description of the tag
- **edgeConnector**: edge connector involved
- **eventframeDefinitions**: events formed from this tag
- **id**: id of the tag
- **isInAssetOpDef**: boolean
- **lastStreamedOn**: last value’s date time
- **mldeployed**: ML model deployed
- **mlexpconfigSet**: many to many ML expconfigs
- **name**: name of the tag
- **parentTags**: parent of this tag
- **ruleDefinitions**:  rule definitions of the tag
- **shortName**: tag short name
- **sourceTag**: this is from where the write back tags get their values
- **spanValue**: 
- **startBatchStep**: 
- **stepcontrolstrategySet**: set of step control strategy
- **stopBatchStep**:
- **tagDataType**: data type of the tag
- **tagProcessType**: process type
- **tagStreamingStatus**: status of straming
- **tagType**: type of the tag among 5 types
- **tagValueType**: type of the value (discrete or continous)
- **tagexpressionSet**: expressions in which tag is used
- **uom**: unit of measurement
- **updatedAt**: updated at date time
- **valueTable**: values of states of tag
- **writeBackTag**: 
- **zeroValue**: specific value

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **alreadyMapped**: Boolean
- **asset**: filter by asset
- **category**: filter by category
- **edgeConnector**: filter by edge connector
- **id**: Filter by ID
- **isWritable**: boolean
- **limit**: Limit number of values in query
- **name__Icontains**: if name contains the string 
- **name__Iexact**: Exact name match the string
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **shortName_Icontains**: if short name contains the string
- **shortName_Iexact**: exact name match the string
- **sourceTag_Name_Icontains**: boolean
- **sourceTag_Name_Iexact**: 
- **tagDataType**: Filter by tag data type
- **tagDataType_In**: filter by tag datatype_In
- **tagProcessType**: Filter by tag process type
- **tagProcessType_In**: 
- **tagsWoAssetPerm**: 
- **tagType**: Filter by tag type
- **tagType_In**: filter by tag type_In
- **tagValueType**: filter by tag value type
- **uom**: filter by uom
- **writeBackTag**: filter by write back tag


TagEtlSheet
^^^^^^^^^^^^^


The available attribtues of this query are as follows:
*******************************************************
- **createdAt**: created at datetime
- **edgeConnector**: Connector it is associated with.
- **etlFile**: Link of the etl file
- **id**: ID of the sheet
- **name**: Name of the sheet
- **sizeInKb**: Size of the sheet in kilobytes
- **updatedAt**: updated at datetime

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **edgeConnector**: Filter by edge connector
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute


TagMeasurements
^^^^^^^^^^^^^^^^^


The available attribtues of this query are as follows:
*******************************************************
- **ahattributeSet**:
- **createdAt**: created at datetime
- **id**: ID of the Measurement
- **name**: Name of the measurement
- **symbol**: Symbol representing the measurement
- **tagSet**:
- **updatedAt**: updated at datetime

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute



NodeInstallers
^^^^^^^^^^^^^^^


The available attribtues of this query are as follows:
*******************************************************

- **buildLocation**: Build location of the node
- **createdAt**: created at datetime
- **deviceBuildStatus**: status of device build
- **dirty**:
- **downloadedOn**: download datetime
- **edgeDevice**: name of the edgeDevice
- **generateCerts**: Certificated generated
- **id**: ID of the installer
- **installedOn**: installed on datetime
- **name**: name of the installer
- **siteVersion**: version of the site
- **sslCertPath**:
- **sslKeyPath**:
- **sslZipPath**:
- **updatedAt**: updated at datetime
- **version**: version of the installer

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **edgeDevice**: Filter by edge device
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute


**Mutations**
----------------



EdgeNodeCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **edgedevice**: created EdgeNode

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newEdgeNode**: Values of different members of the object


EdgeNodeDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **edgedevice**: deleted EdgeNode

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the EdgeNode to be deleted

EdgeNodeUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **edgedevice**: Updated EdgeNode

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateEdgeNode**: Values of different members of the object



EdgeconnectorCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Edgeconnector**: created Edgeconnector

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newEdgeconnector**: Values of different members of the object


EdgeconnectorDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Edgeconnector**: deleted Edgeconnector

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Edgeconnector to be deleted

EdgeconnectorUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Edgeconnector**: Updated Edgeconnector

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateEdgeconnector**: Values of different members of the object



NodeInstallersUpdate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **deviceBuild**: Updated Manualprocedurebatch

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateNodeinstallers**: Values of different members of the object



SiteCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Site**: created Site

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newSite**: Values of different members of the object


SiteDelete
^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Site**: deleted Site

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Site to be deleted

SiteUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Site**: Updated Site

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateSite**: Values of different members of the object


TagCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Tag**: created Tag

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newTag**: Values of different members of the object


TagDelete
^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Tag**: deleted Tag

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Tag to be deleted

TagUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Tag**: Updated Tag

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateTag**: Values of different members of the object



TagetlsheetCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Tagetlsheet**: created Tagetlsheet

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newTagetlsheet**: Values of different members of the object


**Q.Intelligence**
===================

**Queries**
----------------

RuleDefinition
^^^^^^^^^^^^^^^

   

The available attribtues of this query are as follows:
*******************************************************
- **actionDescription**: things to be checked if rule is broken
- **asset**: asset to which it belongs to
- **assetPermission**: assets which have rules access
- **category**: category affected
- **config**: configuration for rule definition
- **createdAt**: created at date time
- **durationMs**: time for which rule is broken
- **edgeConnector**: edge connector involved
- **emailIds**: list of email ids
- **id**: ID of the rule definition
- **isAcknowledgeable**: boolean
- **isActive**: boolean
- **name**: name of the rule definition
- **phoneNumbers**: list of phone numbers
- **product**: product associated
- **rawJson**: UI based JSON
- **ruleJson**: JSON of the rule
- **sendEmails**: boolean
- **sendSms**: Boolean
- **severity**: level of impact
- **source**: origin if the rule
- **stepcontrolstrategySet**: 
- **tags**: tags involved
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **updatedAt**: updated at date time
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte**: less than or equal to updated at datetime



TagExpression
^^^^^^^^^^^^^^^

   

The available attribtues of this query are as follows:
*******************************************************
- **asset**: asset to which it belongs to
- **assetPermission**: permissions pertaining to the tag's asset
- **createdAt**: created at datetime
- **expression**: expression string
- **id**: ID of the expression
- **isStreaming**: boolean
- **needs**: Tags used to build the expression
- **tag**: new tag formed
- **updatedAt**:  updated at datetime
- **workspaceXML**: Blockly XML configuration

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **asset**: filter by asset
- **id**: Filter by ID
- **isStreaming**: filter by streaming expressions
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **tag**: Filter by tag
- **tag_Category**: filter by tag category
- **tag_EdgeConnector**: filter by edge connector
- **tag_EdgeConnector_Isnull**: Filter by connector boolean
- **tag_ShortName_Icontains**:
- **tag_ShortName_Iexact**:
- **updatedAt**: updated at date time
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte**: less than or equal to updated at datetime


EventFrameDefinition
^^^^^^^^^^^^^^^^^^^^^

This query gives the information regarding an event's frame during its duration. 

The available attribtues of this query are as follows:
*******************************************************

- **asset**: asset to which it belongs to
- **assetPermission**: permission of the asset
- **category**: category of definition
- **createdAt**: created at date time
- **id**: ID of the frame
- **name**: name of the frame
- **startDurationMs**: start time for which the rule is to be broken
- **startRawJson**: JSON for start raw
- **startRuleJson**: JSON for start rule
- **stopDurationMs**: stop time for which the rule is to be broken
- **stopRawJson**: JSON for stop raw
- **stopRuleJson**: JSON for stop rule
- **tags**: tags used to build this event
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **updatedAt**: updated at date time
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte**: less than or equal to updated at datetime


MLDeployed
^^^^^^^^^^^^^

This query gives the information about the Machine Learnig Model which is deployed.

The available attribtues of this query are as follows:
*******************************************************
- **assetPermission**: asset permission
- **createdAt**: created at date time
- **id**: ID of the model
- **isActive**: if the model is active
- **mlExperiment**: Ml experiment it corresponds to
- **mlNode**: ML node it corresponds to
- **modelStr**:
- **tag**: associated tag
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **isActive**: boolean
- **isSpectralModel**: boolean
- **limit**: Limit number of values in query
- **mlNode_Id**: Filter by ml node ID
- **mlNode_Isnull**: boolean
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **updatedAt**: updated at date time
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte**: less than or equal to updated at datetime

MLExpConfig
^^^^^^^^^^^^^

   

The available attribtues of this query are as follows:
*******************************************************

- **anomalyRange**:
- **assetPermission**: 
- **createdAt**: created at date time
- **downstreamAssets**:
- **futureWindow**:
- **id**:
- **knownTestAnomalies**: 
- **mlExperiment**:
- **previewRange**:
- **sampledDataset**: 
- **sessionType**:
- **targetTag**:
- **targetTagAsFeature**:
- **testingRange**:
- **trainingRange**:
- **updatedAt**: updated at date time
- **upstreamAssets**:

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute

MLExperiment
^^^^^^^^^^^^^


The available attribtues of this query are as follows:
*******************************************************

- **assetPermission**: asset permission it has
- **configId**: configuration ID
- **createdAt**: created at date time
- **featureTags**: feature tags it has
- **id**: ID
- **mlDeployed**: deployed ML model
- **name**: name 
- **runId**:
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute



Procedure
^^^^^^^^^^^^^

  This query gives the information on the receipe of a Product and a Site.

The available attribtues of this query are as follows:
*******************************************************
- **additionalAttributes**: specify receipe_type, formula, recepie_version
- **batches**: all the batches created for this
- **createdAt**: created at date time
- **id**: ID of the procedure
- **name**: name of the procedure
- **procedureState**: state among 5 values
- **procedureStepNodes**: 
- **product**: product to which it belongs to
- **site**: site to which it is linked with
- **testResults**: 
- **totalBatches**: no. of total batches of this receipe
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **name_Icontains**: if name contains the string
- **name_Iexact**: Exact name match the string
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute
- **procedureState**: filter by state
- **product**: filter by product
- **updatedAt**: updated at date time
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte**: less than or equal to updated at datetime


ProcedureStep
^^^^^^^^^^^^^^

    This query gives the information of one step at a time on the receipe of a Product and a Site.

The available attribtues of this query are as follows:
*******************************************************
- **createdAt**: created at date time
- **id**: id of the procedure step
- **name**: name of the procedure step
- **order**: defines the depth of hierarchy
- **parent**: parent of the procedure step
- **procedure**: procedure to which it refers to
- **procedureStepChildNodes**: no. of child nodes
- **stepComponents**: list of components involved
- **stepType**: among the 5 types defined
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **name_Icontains**: if name contains the string
- **name_Iexact**: Exact name match the string
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute.
- **parent**: filter by parent
- **procedure**: filter by procedure
- **stepType**: filter by step type


ProcedureStepComponent
^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this query are as follows:
*******************************************************
- **asset**: asset to which it belongs to
- **batches**: batches that get formed
- **createdAt**: created at date time
- **deferredData**: gets data deferred from child
- **deferredStartBatchTag**: start batch tag of first child
- **deferredStartRule**: start rule of first child
- **deferredStopBatchTag**: stop batch tag of the first child
- **deferredStopRule**: stop rule of the first child
- **id**: id of the component
- **procedurestepSet**:
- **startBatchTag**:
- **startRuleJson**:
- **stepcontrolstrategySet**:
- **stopBatchTag**: stop batch tag
- **stopRuleJson**: JSON of the stop rule
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **asset**: FIilter by the asset
- **id**: Filter by ID
- **id_Gte**: greater than or equal to ID
- **id_Lte**: Less than or equal to the ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute.
- **updatedAt**: updated at date time
- **updatedAt_Gt**: greater than updated at datetime
- **updatedAt_Gte**: greater than or equal to updated at datetime
- **updatedAt_Lt**: less than updated at datetime
- **updatedAt_Lte**: less than or equal to updated at datetime


StepControlStrategy
^^^^^^^^^^^^^^^^^^^^


The available attribtues of this query are as follows:
*******************************************************
- **childControlStrategy**:  children involved
- **createdAt**: created at date time
- **criticalType**: CQA or CPP type
- **id**: id of the strategy
- **rule**: rule imposed that is to be broken
- **stepComponent**: respective step component
- **stepcontrolstrategySet**: parent of child control strategy
- **tag**: tag which it affects
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute


**Mutations**
----------------


ProcedureCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Procedure**: created Procedure

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newProcedure**: Values of different members of the object


ProcedureDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Procedure**: deleted Procedure

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Procedure to be deleted

ProcedureUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Procedure**: Updated Procedure

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateProcedure**: Values of different members of the object



ProcedureStepCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ProcedureStep**: created ProcedureStep

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newProcedureStep**: Values of different members of the object


ProcedureStepDelete
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ProcedureStep**: deleted ProcedureStep

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the ProcedureStep to be deleted

ProcedureStepUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **ProcedureStep**: Updated ProcedureStep

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateProcedureStep**: Values of different members of the object



ProcedurestepbatchCreate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **procedurestepbatch**: created procedurestepbatch

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newprocedurestepbatch**: Values of different members of the object


ProcedurestepbatchDelete
^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **procedurestepbatch**: deleted procedurestepbatch

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the procedurestepbatch to be deleted

ProcedurestepbatchUpdate
^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **procedurestepbatch**: Updated procedurestepbatch

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateprocedurestepbatch**: Values of different members of the object




ProcedurestepcomponentCreate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **procedurestepcomponent**: created procedurestepcomponent

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newprocedurestepcomponent**: Values of different members of the object


ProcedurestepcomponentUpdate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **procedurestepcomponent**: Updated procedurestepcomponent

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateprocedurestepcomponent**: Values of different members of the object


StepcontrolstrategyCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Stepcontrolstrategy**: created Stepcontrolstrategy

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newStepcontrolstrategy**: Values of different members of the object


StepcontrolstrategyDelete
^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Stepcontrolstrategy**: deleted Stepcontrolstrategy

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Stepcontrolstrategy to be deleted

StepcontrolstrategyUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Stepcontrolstrategy**: Updated Stepcontrolstrategy

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateStepcontrolstrategy**: Values of different members of the object


**Q.Applications**
=======================

**Queries**
----------------
RuleBreak
^^^^^^^^^^^^^^^^^^^^^
EventFrameOccurrence
^^^^^^^^^^^^^^^^^^^^^
ContextFrameOccurence
^^^^^^^^^^^^^^^^^^^^^
Batch
^^^^^^^^^^^^^^^^^^^^^
BatchPhase
^^^^^^^^^^^^^^^^^^^^^

ProcedureStepBatch
^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this query are as follows:
*******************************************************
- **batchName**: name of the batch
- **batchType**: type of the batch
- **createdAt**: created at date time
- **humanVerified**: boolean
- **id**: id of the batch
- **procedureStepComponent**:
- **startTime**: start time of the batch
- **stopTime**: stop time of the batch
- **updatedAt**: updated at date time

The available paramter to filter this query are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **batchName_Icontains**: if batch name contains the string
- **batchName_Iexact**: if batch name contains the exact string
- **id**: Filter by ID
- **limit**: Limit number of values in query
- **offset**: Offset objects by number
- **ordering**: Order results by the attribute.
- **procedureId**: filter by procedure ID
- **productid**: filter by product ID



**Mutations**
----------------

RemoveAssetFromOperationUpdate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **procedureStep**: Updated procedureStep

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateprocedureStep**: Values of different members of the object



RuledefinitionCreate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Ruledefinition**: created Ruledefinition

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **newRuledefinition**: Values of different members of the object


RuledefinitionDelete
^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Ruledefinition**: deleted Ruledefinition

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the Ruledefinition to be deleted

RuledefinitionUpdate
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **Ruledefinition**: Updated Ruledefinition

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **updateRuledefinition**: Values of different members of the object


bulkProcedureBatchDelete
^^^^^^^^^^^^^^^^^^^^^^^^


The available attribtues of this mutation are as follows:
*******************************************************
- **ok**: Tells if the operation is performed

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **batchName**: Name of the batch to be deleted
- **procedureId**: Procedure ID of the batch

--Update
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: Updated --

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **update--**: Values of different members of the object



--Create
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: created --

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **new--**: Values of different members of the object


--Delete
^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: deleted --

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the -- to be deleted

--Update
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: Updated --

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **update--**: Values of different members of the object



--Create
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: created --

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **new--**: Values of different members of the object


--Delete
^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: deleted --

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the -- to be deleted

--Update
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: Updated --

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **update--**: Values of different members of the object



--Create
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: created --

The available paramters for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **new--**: Values of different members of the object


--Delete
^^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: deleted --

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **id**: ID of the -- to be deleted

--Update
^^^^^^^^^^^^^^^^^^^^

   

The available attribtues of this mutation are as follows:
*******************************************************
- **errors**: Info of any error occurred
- **ok**: Tells if the operation is performed
- **--**: Updated --

The available paramter for this mutation are as follows:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **update--**: Values of different members of the object



**Others**
=======================


**Examples**
----------------

Setup Data Source
^^^^^^^^^^^^^^^^^^


**DataTypes**
----------------

Int 
^^^

customDateTime
^^^^^^^^^^^^^^^
