```mermaid
classDiagram
    %% DOMAINS
    class domain_01{
        <<domain>>
    }
    class domain_02{
        <<domain>>
    }
    class domain_03{
        <<domain>>
    }
    class domain_04{
        <<domain>>
    }
    class domain_05{
        <<domain>>
    }
    class domain_06{
        <<domain>>
    }
    class domain_07{
        <<domain>>
    }
    class domain_08{
        <<domain>>
    }
    class domain_09{
        <<domain>>
    }
    class domain_10{
        <<domain>>
    }
    class domain_11{
        <<domain>>
    }
    class domain_12{
        <<domain>>
    }
    class domain_13{
        <<domain>>
    }
    class domain_14{
        <<domain>>
    }
    class domain_15{
        <<domain>>
    }
    class domain_16{
        <<domain>>
    }
    class domain_17{
        <<domain>>
    }
    class domain_18{
        <<domain>>
    }
    class domain_19{
        <<domain>>
    }
    class domain_20{
        <<domain>>
    }
    %% OWNERSHIP
    domain_01 --> domain_01_src : owns
    domain_01 --> domain_01_cur : owns
    domain_01 --> domain_01_con : owns
    domain_02 --> domain_02_src : owns
    domain_02 --> domain_02_cur : owns
    domain_02 --> domain_02_con : owns
    domain_03 --> domain_03_src : owns
    domain_03 --> domain_03_cur : owns
    domain_03 --> domain_03_con : owns
    domain_04 --> domain_04_src : owns
    domain_04 --> domain_04_cur : owns
    domain_04 --> domain_04_con : owns
    domain_05 --> domain_05_src : owns
    domain_05 --> domain_05_cur : owns
    domain_05 --> domain_05_con : owns
    domain_06 --> domain_06_src : owns
    domain_06 --> domain_06_cur : owns
    domain_06 --> domain_06_con : owns
    domain_07 --> domain_07_src : owns
    domain_07 --> domain_07_cur : owns
    domain_07 --> domain_07_con : owns
    domain_08 --> domain_08_src : owns
    domain_08 --> domain_08_cur : owns
    domain_08 --> domain_08_con : owns
    domain_09 --> domain_09_src : owns
    domain_09 --> domain_09_cur : owns
    domain_09 --> domain_09_con : owns
    domain_10 --> domain_10_src : owns
    domain_10 --> domain_10_cur : owns
    domain_10 --> domain_10_con : owns
    domain_11 --> domain_11_src : owns
    domain_11 --> domain_11_cur : owns
    domain_11 --> domain_11_con : owns
    domain_12 --> domain_12_src : owns
    domain_12 --> domain_12_cur : owns
    domain_12 --> domain_12_con : owns
    domain_13 --> domain_13_src : owns
    domain_13 --> domain_13_cur : owns
    domain_13 --> domain_13_con : owns
    domain_14 --> domain_14_src : owns
    domain_14 --> domain_14_cur : owns
    domain_14 --> domain_14_con : owns
    domain_15 --> domain_15_src : owns
    domain_15 --> domain_15_cur : owns
    domain_15 --> domain_15_con : owns
    domain_16 --> domain_16_src : owns
    domain_16 --> domain_16_cur : owns
    domain_16 --> domain_16_con : owns
    domain_17 --> domain_17_src : owns
    domain_17 --> domain_17_cur : owns
    domain_17 --> domain_17_con : owns
    domain_18 --> domain_18_src : owns
    domain_18 --> domain_18_cur : owns
    domain_18 --> domain_18_con : owns
    domain_19 --> domain_19_src : owns
    domain_19 --> domain_19_cur : owns
    domain_19 --> domain_19_con : owns
    domain_20 --> domain_20_src : owns
    domain_20 --> domain_20_cur : owns
    domain_20 --> domain_20_con : owns
    %% SOURCE ALIGNED DATA PRODUCTS
    domain_01_src --> domain_01_src_schema : exposes
    class domain_01_src{
        <<data-product>>
        dataProductBusinessName : Domain 01 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_01_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_02_src --> domain_02_src_schema : exposes
    class domain_02_src{
        <<data-product>>
        dataProductBusinessName : Domain 02 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_02_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_03_src --> domain_03_src_schema : exposes
    class domain_03_src{
        <<data-product>>
        dataProductBusinessName : Domain 03 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_03_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_04_src --> domain_04_src_schema : exposes
    class domain_04_src{
        <<data-product>>
        dataProductBusinessName : Domain 04 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_04_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_05_src --> domain_05_src_schema : exposes
    class domain_05_src{
        <<data-product>>
        dataProductBusinessName : Domain 05 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_05_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_06_src --> domain_06_src_schema : exposes
    class domain_06_src{
        <<data-product>>
        dataProductBusinessName : Domain 06 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_06_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_07_src --> domain_07_src_schema : exposes
    class domain_07_src{
        <<data-product>>
        dataProductBusinessName : Domain 07 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_07_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_08_src --> domain_08_src_schema : exposes
    class domain_08_src{
        <<data-product>>
        dataProductBusinessName : Domain 08 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_08_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_09_src --> domain_09_src_schema : exposes
    class domain_09_src{
        <<data-product>>
        dataProductBusinessName : Domain 09 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_09_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_10_src --> domain_10_src_schema : exposes
    class domain_10_src{
        <<data-product>>
        dataProductBusinessName : Domain 10 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_10_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_11_src --> domain_11_src_schema : exposes
    class domain_11_src{
        <<data-product>>
        dataProductBusinessName : Domain 11 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_11_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_12_src --> domain_12_src_schema : exposes
    class domain_12_src{
        <<data-product>>
        dataProductBusinessName : Domain 12 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_12_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_13_src --> domain_13_src_schema : exposes
    class domain_13_src{
        <<data-product>>
        dataProductBusinessName : Domain 13 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_13_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_14_src --> domain_14_src_schema : exposes
    class domain_14_src{
        <<data-product>>
        dataProductBusinessName : Domain 14 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_14_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_15_src --> domain_15_src_schema : exposes
    class domain_15_src{
        <<data-product>>
        dataProductBusinessName : Domain 15 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_15_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_16_src --> domain_16_src_schema : exposes
    class domain_16_src{
        <<data-product>>
        dataProductBusinessName : Domain 16 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_16_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_17_src --> domain_17_src_schema : exposes
    class domain_17_src{
        <<data-product>>
        dataProductBusinessName : Domain 17 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_17_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_18_src --> domain_18_src_schema : exposes
    class domain_18_src{
        <<data-product>>
        dataProductBusinessName : Domain 18 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_18_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_19_src --> domain_19_src_schema : exposes
    class domain_19_src{
        <<data-product>>
        dataProductBusinessName : Domain 19 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_19_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    domain_20_src --> domain_20_src_schema : exposes
    class domain_20_src{
        <<data-product>>
        dataProductBusinessName : Domain 20 Source Aligned
        dataProductTier : sourceAligned
    }
    class domain_20_src_schema{
        <<data-contract-schema>>
        id : string
        value : number
    }
    %% CURATED DATA PRODUCTS
    domain_01_cur --> domain_01_cur_schema : exposes
    class domain_01_cur{
        <<data-product>>
        dataProductBusinessName : Domain 01 Curated
        dataProductTier : curated
    }
    class domain_01_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_02_cur --> domain_02_cur_schema : exposes
    class domain_02_cur{
        <<data-product>>
        dataProductBusinessName : Domain 02 Curated
        dataProductTier : curated
    }
    class domain_02_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_03_cur --> domain_03_cur_schema : exposes
    class domain_03_cur{
        <<data-product>>
        dataProductBusinessName : Domain 03 Curated
        dataProductTier : curated
    }
    class domain_03_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_04_cur --> domain_04_cur_schema : exposes
    class domain_04_cur{
        <<data-product>>
        dataProductBusinessName : Domain 04 Curated
        dataProductTier : curated
    }
    class domain_04_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_05_cur --> domain_05_cur_schema : exposes
    class domain_05_cur{
        <<data-product>>
        dataProductBusinessName : Domain 05 Curated
        dataProductTier : curated
    }
    class domain_05_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_06_cur --> domain_06_cur_schema : exposes
    class domain_06_cur{
        <<data-product>>
        dataProductBusinessName : Domain 06 Curated
        dataProductTier : curated
    }
    class domain_06_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_07_cur --> domain_07_cur_schema : exposes
    class domain_07_cur{
        <<data-product>>
        dataProductBusinessName : Domain 07 Curated
        dataProductTier : curated
    }
    class domain_07_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_08_cur --> domain_08_cur_schema : exposes
    class domain_08_cur{
        <<data-product>>
        dataProductBusinessName : Domain 08 Curated
        dataProductTier : curated
    }
    class domain_08_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_09_cur --> domain_09_cur_schema : exposes
    class domain_09_cur{
        <<data-product>>
        dataProductBusinessName : Domain 09 Curated
        dataProductTier : curated
    }
    class domain_09_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_10_cur --> domain_10_cur_schema : exposes
    class domain_10_cur{
        <<data-product>>
        dataProductBusinessName : Domain 10 Curated
        dataProductTier : curated
    }
    class domain_10_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_11_cur --> domain_11_cur_schema : exposes
    class domain_11_cur{
        <<data-product>>
        dataProductBusinessName : Domain 11 Curated
        dataProductTier : curated
    }
    class domain_11_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_12_cur --> domain_12_cur_schema : exposes
    class domain_12_cur{
        <<data-product>>
        dataProductBusinessName : Domain 12 Curated
        dataProductTier : curated
    }
    class domain_12_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_13_cur --> domain_13_cur_schema : exposes
    class domain_13_cur{
        <<data-product>>
        dataProductBusinessName : Domain 13 Curated
        dataProductTier : curated
    }
    class domain_13_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_14_cur --> domain_14_cur_schema : exposes
    class domain_14_cur{
        <<data-product>>
        dataProductBusinessName : Domain 14 Curated
        dataProductTier : curated
    }
    class domain_14_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_15_cur --> domain_15_cur_schema : exposes
    class domain_15_cur{
        <<data-product>>
        dataProductBusinessName : Domain 15 Curated
        dataProductTier : curated
    }
    class domain_15_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_16_cur --> domain_16_cur_schema : exposes
    class domain_16_cur{
        <<data-product>>
        dataProductBusinessName : Domain 16 Curated
        dataProductTier : curated
    }
    class domain_16_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_17_cur --> domain_17_cur_schema : exposes
    class domain_17_cur{
        <<data-product>>
        dataProductBusinessName : Domain 17 Curated
        dataProductTier : curated
    }
    class domain_17_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_18_cur --> domain_18_cur_schema : exposes
    class domain_18_cur{
        <<data-product>>
        dataProductBusinessName : Domain 18 Curated
        dataProductTier : curated
    }
    class domain_18_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_19_cur --> domain_19_cur_schema : exposes
    class domain_19_cur{
        <<data-product>>
        dataProductBusinessName : Domain 19 Curated
        dataProductTier : curated
    }
    class domain_19_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    domain_20_cur --> domain_20_cur_schema : exposes
    class domain_20_cur{
        <<data-product>>
        dataProductBusinessName : Domain 20 Curated
        dataProductTier : curated
    }
    class domain_20_cur_schema{
        <<data-contract-schema>>
        id : string
        value : number
        status : string
    }
    %% CONSUMER ALIGNED DATA PRODUCTS
    domain_01_con --> domain_01_con_schema : exposes
    class domain_01_con{
        <<data-product>>
        dataProductBusinessName : Domain 01 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_01_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_02_con --> domain_02_con_schema : exposes
    class domain_02_con{
        <<data-product>>
        dataProductBusinessName : Domain 02 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_02_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_03_con --> domain_03_con_schema : exposes
    class domain_03_con{
        <<data-product>>
        dataProductBusinessName : Domain 03 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_03_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_04_con --> domain_04_con_schema : exposes
    class domain_04_con{
        <<data-product>>
        dataProductBusinessName : Domain 04 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_04_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_05_con --> domain_05_con_schema : exposes
    class domain_05_con{
        <<data-product>>
        dataProductBusinessName : Domain 05 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_05_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_06_con --> domain_06_con_schema : exposes
    class domain_06_con{
        <<data-product>>
        dataProductBusinessName : Domain 06 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_06_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_07_con --> domain_07_con_schema : exposes
    class domain_07_con{
        <<data-product>>
        dataProductBusinessName : Domain 07 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_07_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_08_con --> domain_08_con_schema : exposes
    class domain_08_con{
        <<data-product>>
        dataProductBusinessName : Domain 08 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_08_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_09_con --> domain_09_con_schema : exposes
    class domain_09_con{
        <<data-product>>
        dataProductBusinessName : Domain 09 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_09_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_10_con --> domain_10_con_schema : exposes
    class domain_10_con{
        <<data-product>>
        dataProductBusinessName : Domain 10 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_10_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_11_con --> domain_11_con_schema : exposes
    class domain_11_con{
        <<data-product>>
        dataProductBusinessName : Domain 11 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_11_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_12_con --> domain_12_con_schema : exposes
    class domain_12_con{
        <<data-product>>
        dataProductBusinessName : Domain 12 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_12_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_13_con --> domain_13_con_schema : exposes
    class domain_13_con{
        <<data-product>>
        dataProductBusinessName : Domain 13 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_13_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_14_con --> domain_14_con_schema : exposes
    class domain_14_con{
        <<data-product>>
        dataProductBusinessName : Domain 14 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_14_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_15_con --> domain_15_con_schema : exposes
    class domain_15_con{
        <<data-product>>
        dataProductBusinessName : Domain 15 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_15_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_16_con --> domain_16_con_schema : exposes
    class domain_16_con{
        <<data-product>>
        dataProductBusinessName : Domain 16 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_16_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_17_con --> domain_17_con_schema : exposes
    class domain_17_con{
        <<data-product>>
        dataProductBusinessName : Domain 17 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_17_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_18_con --> domain_18_con_schema : exposes
    class domain_18_con{
        <<data-product>>
        dataProductBusinessName : Domain 18 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_18_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_19_con --> domain_19_con_schema : exposes
    class domain_19_con{
        <<data-product>>
        dataProductBusinessName : Domain 19 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_19_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    domain_20_con --> domain_20_con_schema : exposes
    class domain_20_con{
        <<data-product>>
        dataProductBusinessName : Domain 20 Consumer Aligned
        dataProductTier : consumerAligned
    }
    class domain_20_con_schema{
        <<data-contract-schema>>
        id : string
        aggregated_value : number
    }
    %% DEPENDENCIES
    domain_01_src --> domain_01_cur : provides
    domain_01_cur --> domain_01_con : provides
    domain_02_src --> domain_02_cur : provides
    domain_02_cur --> domain_02_con : provides
    domain_03_src --> domain_03_cur : provides
    domain_03_cur --> domain_03_con : provides
    domain_04_src --> domain_04_cur : provides
    domain_04_cur --> domain_04_con : provides
    domain_05_src --> domain_05_cur : provides
    domain_05_cur --> domain_05_con : provides
    domain_06_src --> domain_06_cur : provides
    domain_06_cur --> domain_06_con : provides
    domain_07_src --> domain_07_cur : provides
    domain_07_cur --> domain_07_con : provides
    domain_08_src --> domain_08_cur : provides
    domain_08_cur --> domain_08_con : provides
    domain_09_src --> domain_09_cur : provides
    domain_09_cur --> domain_09_con : provides
    domain_10_src --> domain_10_cur : provides
    domain_10_cur --> domain_10_con : provides
    domain_11_src --> domain_11_cur : provides
    domain_11_cur --> domain_11_con : provides
    domain_12_src --> domain_12_cur : provides
    domain_12_cur --> domain_12_con : provides
    domain_13_src --> domain_13_cur : provides
    domain_13_cur --> domain_13_con : provides
    domain_14_src --> domain_14_cur : provides
    domain_14_cur --> domain_14_con : provides
    domain_15_src --> domain_15_cur : provides
    domain_15_cur --> domain_15_con : provides
    domain_16_src --> domain_16_cur : provides
    domain_16_cur --> domain_16_con : provides
    domain_17_src --> domain_17_cur : provides
    domain_17_cur --> domain_17_con : provides
    domain_18_src --> domain_18_cur : provides
    domain_18_cur --> domain_18_con : provides
    domain_19_src --> domain_19_cur : provides
    domain_19_cur --> domain_19_con : provides
    domain_20_src --> domain_20_cur : provides
    domain_20_cur --> domain_20_con : provides
```
