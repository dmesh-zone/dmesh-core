```mermaid
classDiagram
    %% DOMAIN
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
    domain_01 --> inventory_src_1: owns
    domain_02 --> inventory_src_2: owns
    domain_03 --> inventory_src_3: owns
    domain_04 --> inventory_src_4: owns
    domain_05 --> inventory_src_5: owns
    domain_06 --> inventory_src_6: owns
    domain_07 --> inventory_src_7: owns
    domain_08 --> inventory_src_8: owns
    domain_09 --> inventory_src_9: owns
    domain_10 --> inventory_src_10: owns
    domain_01 --> inventory_src_11: owns
    domain_02 --> inventory_src_12: owns
    domain_03 --> inventory_src_13: owns
    domain_04 --> inventory_src_14: owns
    domain_05 --> inventory_src_15: owns
    domain_06 --> inventory_src_16: owns
    domain_07 --> inventory_src_17: owns
    domain_08 --> inventory_src_18: owns
    domain_09 --> inventory_src_19: owns
    domain_10 --> inventory_src_20: owns
    domain_01 --> inventory_src_21: owns
    domain_02 --> inventory_src_22: owns
    domain_03 --> inventory_src_23: owns
    domain_04 --> inventory_src_24: owns
    domain_05 --> inventory_src_25: owns
    domain_06 --> inventory_src_26: owns
    domain_07 --> inventory_src_27: owns
    domain_08 --> inventory_src_28: owns
    domain_09 --> inventory_src_29: owns
    domain_10 --> inventory_src_30: owns
    domain_01 --> inventory_src_31: owns
    domain_02 --> inventory_src_32: owns
    domain_03 --> inventory_src_33: owns
    domain_04 --> inventory_src_34: owns
    domain_05 --> inventory_src_35: owns
    domain_06 --> inventory_src_36: owns
    domain_07 --> inventory_src_37: owns
    domain_08 --> inventory_src_38: owns
    domain_09 --> inventory_src_39: owns
    domain_10 --> inventory_src_40: owns
    domain_01 --> inventory_src_41: owns
    domain_02 --> inventory_src_42: owns
    domain_03 --> inventory_src_43: owns
    domain_04 --> inventory_src_44: owns
    domain_05 --> inventory_src_45: owns
    domain_06 --> inventory_src_46: owns
    domain_07 --> inventory_src_47: owns
    domain_08 --> inventory_src_48: owns
    domain_09 --> inventory_src_49: owns
    domain_10 --> inventory_src_50: owns
    domain_01 --> inventory_cur_1: owns
    domain_02 --> inventory_cur_2: owns
    domain_03 --> inventory_cur_3: owns
    domain_04 --> inventory_cur_4: owns
    domain_05 --> inventory_cur_5: owns
    domain_06 --> inventory_cur_6: owns
    domain_07 --> inventory_cur_7: owns
    domain_08 --> inventory_cur_8: owns
    domain_09 --> inventory_cur_9: owns
    domain_10 --> inventory_cur_10: owns
    domain_01 --> inventory_cur_11: owns
    domain_02 --> inventory_cur_12: owns
    domain_03 --> inventory_cur_13: owns
    domain_04 --> inventory_cur_14: owns
    domain_05 --> inventory_cur_15: owns
    domain_06 --> inventory_con_1: owns
    domain_07 --> inventory_con_2: owns
    domain_08 --> inventory_con_3: owns
    domain_09 --> inventory_con_4: owns
    domain_10 --> inventory_con_5: owns
    domain_01 --> inventory_con_6: owns
    domain_02 --> inventory_con_7: owns
    domain_03 --> inventory_con_8: owns
    domain_04 --> inventory_con_9: owns
    domain_05 --> inventory_con_10: owns
    domain_06 --> inventory_con_11: owns
    domain_07 --> inventory_con_12: owns
    domain_08 --> inventory_con_13: owns
    domain_09 --> inventory_con_14: owns
    domain_10 --> inventory_con_15: owns
    domain_01 --> inventory_con_16: owns
    domain_02 --> inventory_con_17: owns
    domain_03 --> inventory_con_18: owns
    domain_04 --> inventory_con_19: owns
    domain_05 --> inventory_con_20: owns
    domain_06 --> sales_src_1: owns
    domain_07 --> sales_src_2: owns
    domain_08 --> sales_src_3: owns
    domain_09 --> sales_src_4: owns
    domain_10 --> sales_src_5: owns
    domain_01 --> sales_src_6: owns
    domain_02 --> sales_src_7: owns
    domain_03 --> sales_src_8: owns
    domain_04 --> sales_src_9: owns
    domain_05 --> sales_src_10: owns
    domain_06 --> sales_src_11: owns
    domain_07 --> sales_src_12: owns
    domain_08 --> sales_src_13: owns
    domain_09 --> sales_src_14: owns
    domain_10 --> sales_src_15: owns
    domain_01 --> sales_src_16: owns
    domain_02 --> sales_src_17: owns
    domain_03 --> sales_src_18: owns
    domain_04 --> sales_src_19: owns
    domain_05 --> sales_src_20: owns
    domain_06 --> sales_src_21: owns
    domain_07 --> sales_src_22: owns
    domain_08 --> sales_src_23: owns
    domain_09 --> sales_src_24: owns
    domain_10 --> sales_src_25: owns
    domain_01 --> sales_src_26: owns
    domain_02 --> sales_src_27: owns
    domain_03 --> sales_src_28: owns
    domain_04 --> sales_src_29: owns
    domain_05 --> sales_src_30: owns
    domain_06 --> sales_src_31: owns
    domain_07 --> sales_src_32: owns
    domain_08 --> sales_src_33: owns
    domain_09 --> sales_src_34: owns
    domain_10 --> sales_src_35: owns
    domain_01 --> sales_src_36: owns
    domain_02 --> sales_src_37: owns
    domain_03 --> sales_src_38: owns
    domain_04 --> sales_src_39: owns
    domain_05 --> sales_src_40: owns
    domain_06 --> sales_src_41: owns
    domain_07 --> sales_src_42: owns
    domain_08 --> sales_src_43: owns
    domain_09 --> sales_src_44: owns
    domain_10 --> sales_src_45: owns
    domain_01 --> sales_src_46: owns
    domain_02 --> sales_src_47: owns
    domain_03 --> sales_src_48: owns
    domain_04 --> sales_src_49: owns
    domain_05 --> sales_src_50: owns
    domain_06 --> sales_cur_1: owns
    domain_07 --> sales_cur_2: owns
    domain_08 --> sales_cur_3: owns
    domain_09 --> sales_cur_4: owns
    domain_10 --> sales_cur_5: owns
    domain_01 --> sales_cur_6: owns
    domain_02 --> sales_cur_7: owns
    domain_03 --> sales_cur_8: owns
    domain_04 --> sales_cur_9: owns
    domain_05 --> sales_cur_10: owns
    domain_06 --> sales_cur_11: owns
    domain_07 --> sales_cur_12: owns
    domain_08 --> sales_cur_13: owns
    domain_09 --> sales_cur_14: owns
    domain_10 --> sales_cur_15: owns
    domain_01 --> sales_con_1: owns
    domain_02 --> sales_con_2: owns
    domain_03 --> sales_con_3: owns
    domain_04 --> sales_con_4: owns
    domain_05 --> sales_con_5: owns
    domain_06 --> sales_con_6: owns
    domain_07 --> sales_con_7: owns
    domain_08 --> sales_con_8: owns
    domain_09 --> sales_con_9: owns
    domain_10 --> sales_con_10: owns
    domain_01 --> sales_con_11: owns
    domain_02 --> sales_con_12: owns
    domain_03 --> sales_con_13: owns
    domain_04 --> sales_con_14: owns
    domain_05 --> sales_con_15: owns
    domain_06 --> sales_con_16: owns
    domain_07 --> sales_con_17: owns
    domain_08 --> sales_con_18: owns
    domain_09 --> sales_con_19: owns
    domain_10 --> sales_con_20: owns
    domain_01 --> customer_src_1: owns
    domain_02 --> customer_src_2: owns
    domain_03 --> customer_src_3: owns
    domain_04 --> customer_src_4: owns
    domain_05 --> customer_src_5: owns
    domain_06 --> customer_src_6: owns
    domain_07 --> customer_src_7: owns
    domain_08 --> customer_src_8: owns
    domain_09 --> customer_src_9: owns
    domain_10 --> customer_src_10: owns
    domain_01 --> customer_src_11: owns
    domain_02 --> customer_src_12: owns
    domain_03 --> customer_src_13: owns
    domain_04 --> customer_src_14: owns
    domain_05 --> customer_src_15: owns
    domain_06 --> customer_src_16: owns
    domain_07 --> customer_src_17: owns
    domain_08 --> customer_src_18: owns
    domain_09 --> customer_src_19: owns
    domain_10 --> customer_src_20: owns
    domain_01 --> customer_src_21: owns
    domain_02 --> customer_src_22: owns
    domain_03 --> customer_src_23: owns
    domain_04 --> customer_src_24: owns
    domain_05 --> customer_src_25: owns
    domain_06 --> customer_src_26: owns
    domain_07 --> customer_src_27: owns
    domain_08 --> customer_src_28: owns
    domain_09 --> customer_src_29: owns
    domain_10 --> customer_src_30: owns
    domain_01 --> customer_src_31: owns
    domain_02 --> customer_src_32: owns
    domain_03 --> customer_src_33: owns
    domain_04 --> customer_src_34: owns
    domain_05 --> customer_src_35: owns
    domain_06 --> customer_src_36: owns
    domain_07 --> customer_src_37: owns
    domain_08 --> customer_src_38: owns
    domain_09 --> customer_src_39: owns
    domain_10 --> customer_src_40: owns
    domain_01 --> customer_src_41: owns
    domain_02 --> customer_src_42: owns
    domain_03 --> customer_src_43: owns
    domain_04 --> customer_src_44: owns
    domain_05 --> customer_src_45: owns
    domain_06 --> customer_src_46: owns
    domain_07 --> customer_src_47: owns
    domain_08 --> customer_src_48: owns
    domain_09 --> customer_src_49: owns
    domain_10 --> customer_src_50: owns
    domain_01 --> customer_cur_1: owns
    domain_02 --> customer_cur_2: owns
    domain_03 --> customer_cur_3: owns
    domain_04 --> customer_cur_4: owns
    domain_05 --> customer_cur_5: owns
    domain_06 --> customer_cur_6: owns
    domain_07 --> customer_cur_7: owns
    domain_08 --> customer_cur_8: owns
    domain_09 --> customer_cur_9: owns
    domain_10 --> customer_cur_10: owns
    domain_01 --> customer_cur_11: owns
    domain_02 --> customer_cur_12: owns
    domain_03 --> customer_cur_13: owns
    domain_04 --> customer_cur_14: owns
    domain_05 --> customer_cur_15: owns
    domain_06 --> customer_con_1: owns
    domain_07 --> customer_con_2: owns
    domain_08 --> customer_con_3: owns
    domain_09 --> customer_con_4: owns
    domain_10 --> customer_con_5: owns
    domain_01 --> customer_con_6: owns
    domain_02 --> customer_con_7: owns
    domain_03 --> customer_con_8: owns
    domain_04 --> customer_con_9: owns
    domain_05 --> customer_con_10: owns
    domain_06 --> customer_con_11: owns
    domain_07 --> customer_con_12: owns
    domain_08 --> customer_con_13: owns
    domain_09 --> customer_con_14: owns
    domain_10 --> customer_con_15: owns
    domain_01 --> customer_con_16: owns
    domain_02 --> customer_con_17: owns
    domain_03 --> customer_con_18: owns
    domain_04 --> customer_con_19: owns
    domain_05 --> customer_con_20: owns
    %% SOURCE ALIGNED DATA PRODUCT
    class inventory_src_1{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 1
    dataProductTier : sourceAligned
    }
    class inventory_src_2{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 2
    dataProductTier : sourceAligned
    }
    class inventory_src_3{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 3
    dataProductTier : sourceAligned
    }
    class inventory_src_4{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 4
    dataProductTier : sourceAligned
    }
    class inventory_src_5{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 5
    dataProductTier : sourceAligned
    }
    class inventory_src_6{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 6
    dataProductTier : sourceAligned
    }
    class inventory_src_7{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 7
    dataProductTier : sourceAligned
    }
    class inventory_src_8{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 8
    dataProductTier : sourceAligned
    }
    class inventory_src_9{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 9
    dataProductTier : sourceAligned
    }
    class inventory_src_10{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 10
    dataProductTier : sourceAligned
    }
    class inventory_src_11{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 11
    dataProductTier : sourceAligned
    }
    class inventory_src_12{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 12
    dataProductTier : sourceAligned
    }
    class inventory_src_13{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 13
    dataProductTier : sourceAligned
    }
    class inventory_src_14{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 14
    dataProductTier : sourceAligned
    }
    class inventory_src_15{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 15
    dataProductTier : sourceAligned
    }
    class inventory_src_16{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 16
    dataProductTier : sourceAligned
    }
    class inventory_src_17{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 17
    dataProductTier : sourceAligned
    }
    class inventory_src_18{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 18
    dataProductTier : sourceAligned
    }
    class inventory_src_19{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 19
    dataProductTier : sourceAligned
    }
    class inventory_src_20{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 20
    dataProductTier : sourceAligned
    }
    class inventory_src_21{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 21
    dataProductTier : sourceAligned
    }
    class inventory_src_22{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 22
    dataProductTier : sourceAligned
    }
    class inventory_src_23{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 23
    dataProductTier : sourceAligned
    }
    class inventory_src_24{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 24
    dataProductTier : sourceAligned
    }
    class inventory_src_25{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 25
    dataProductTier : sourceAligned
    }
    class inventory_src_26{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 26
    dataProductTier : sourceAligned
    }
    class inventory_src_27{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 27
    dataProductTier : sourceAligned
    }
    class inventory_src_28{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 28
    dataProductTier : sourceAligned
    }
    class inventory_src_29{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 29
    dataProductTier : sourceAligned
    }
    class inventory_src_30{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 30
    dataProductTier : sourceAligned
    }
    class inventory_src_31{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 31
    dataProductTier : sourceAligned
    }
    class inventory_src_32{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 32
    dataProductTier : sourceAligned
    }
    class inventory_src_33{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 33
    dataProductTier : sourceAligned
    }
    class inventory_src_34{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 34
    dataProductTier : sourceAligned
    }
    class inventory_src_35{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 35
    dataProductTier : sourceAligned
    }
    class inventory_src_36{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 36
    dataProductTier : sourceAligned
    }
    class inventory_src_37{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 37
    dataProductTier : sourceAligned
    }
    class inventory_src_38{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 38
    dataProductTier : sourceAligned
    }
    class inventory_src_39{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 39
    dataProductTier : sourceAligned
    }
    class inventory_src_40{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 40
    dataProductTier : sourceAligned
    }
    class inventory_src_41{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 41
    dataProductTier : sourceAligned
    }
    class inventory_src_42{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 42
    dataProductTier : sourceAligned
    }
    class inventory_src_43{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 43
    dataProductTier : sourceAligned
    }
    class inventory_src_44{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 44
    dataProductTier : sourceAligned
    }
    class inventory_src_45{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 45
    dataProductTier : sourceAligned
    }
    class inventory_src_46{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 46
    dataProductTier : sourceAligned
    }
    class inventory_src_47{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 47
    dataProductTier : sourceAligned
    }
    class inventory_src_48{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 48
    dataProductTier : sourceAligned
    }
    class inventory_src_49{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 49
    dataProductTier : sourceAligned
    }
    class inventory_src_50{
    <<data-product>>
    dataProductBusinessName : INVENTORY Source 50
    dataProductTier : sourceAligned
    }
    class inventory_cur_1{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 1
    dataProductTier : curated
    }
    class inventory_cur_2{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 2
    dataProductTier : curated
    }
    class inventory_cur_3{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 3
    dataProductTier : curated
    }
    class inventory_cur_4{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 4
    dataProductTier : curated
    }
    class inventory_cur_5{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 5
    dataProductTier : curated
    }
    class inventory_cur_6{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 6
    dataProductTier : curated
    }
    class inventory_cur_7{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 7
    dataProductTier : curated
    }
    class inventory_cur_8{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 8
    dataProductTier : curated
    }
    class inventory_cur_9{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 9
    dataProductTier : curated
    }
    class inventory_cur_10{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 10
    dataProductTier : curated
    }
    class inventory_cur_11{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 11
    dataProductTier : curated
    }
    class inventory_cur_12{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 12
    dataProductTier : curated
    }
    class inventory_cur_13{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 13
    dataProductTier : curated
    }
    class inventory_cur_14{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 14
    dataProductTier : curated
    }
    class inventory_cur_15{
    <<data-product>>
    dataProductBusinessName : INVENTORY Curated 15
    dataProductTier : curated
    }
    class inventory_con_1{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 1
    dataProductTier : consumerAligned
    }
    class inventory_con_2{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 2
    dataProductTier : consumerAligned
    }
    class inventory_con_3{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 3
    dataProductTier : consumerAligned
    }
    class inventory_con_4{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 4
    dataProductTier : consumerAligned
    }
    class inventory_con_5{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 5
    dataProductTier : consumerAligned
    }
    class inventory_con_6{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 6
    dataProductTier : consumerAligned
    }
    class inventory_con_7{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 7
    dataProductTier : consumerAligned
    }
    class inventory_con_8{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 8
    dataProductTier : consumerAligned
    }
    class inventory_con_9{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 9
    dataProductTier : consumerAligned
    }
    class inventory_con_10{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 10
    dataProductTier : consumerAligned
    }
    class inventory_con_11{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 11
    dataProductTier : consumerAligned
    }
    class inventory_con_12{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 12
    dataProductTier : consumerAligned
    }
    class inventory_con_13{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 13
    dataProductTier : consumerAligned
    }
    class inventory_con_14{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 14
    dataProductTier : consumerAligned
    }
    class inventory_con_15{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 15
    dataProductTier : consumerAligned
    }
    class inventory_con_16{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 16
    dataProductTier : consumerAligned
    }
    class inventory_con_17{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 17
    dataProductTier : consumerAligned
    }
    class inventory_con_18{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 18
    dataProductTier : consumerAligned
    }
    class inventory_con_19{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 19
    dataProductTier : consumerAligned
    }
    class inventory_con_20{
    <<data-product>>
    dataProductBusinessName : INVENTORY Consumer 20
    dataProductTier : consumerAligned
    }
    class sales_src_1{
    <<data-product>>
    dataProductBusinessName : SALES Source 1
    dataProductTier : sourceAligned
    }
    class sales_src_2{
    <<data-product>>
    dataProductBusinessName : SALES Source 2
    dataProductTier : sourceAligned
    }
    class sales_src_3{
    <<data-product>>
    dataProductBusinessName : SALES Source 3
    dataProductTier : sourceAligned
    }
    class sales_src_4{
    <<data-product>>
    dataProductBusinessName : SALES Source 4
    dataProductTier : sourceAligned
    }
    class sales_src_5{
    <<data-product>>
    dataProductBusinessName : SALES Source 5
    dataProductTier : sourceAligned
    }
    class sales_src_6{
    <<data-product>>
    dataProductBusinessName : SALES Source 6
    dataProductTier : sourceAligned
    }
    class sales_src_7{
    <<data-product>>
    dataProductBusinessName : SALES Source 7
    dataProductTier : sourceAligned
    }
    class sales_src_8{
    <<data-product>>
    dataProductBusinessName : SALES Source 8
    dataProductTier : sourceAligned
    }
    class sales_src_9{
    <<data-product>>
    dataProductBusinessName : SALES Source 9
    dataProductTier : sourceAligned
    }
    class sales_src_10{
    <<data-product>>
    dataProductBusinessName : SALES Source 10
    dataProductTier : sourceAligned
    }
    class sales_src_11{
    <<data-product>>
    dataProductBusinessName : SALES Source 11
    dataProductTier : sourceAligned
    }
    class sales_src_12{
    <<data-product>>
    dataProductBusinessName : SALES Source 12
    dataProductTier : sourceAligned
    }
    class sales_src_13{
    <<data-product>>
    dataProductBusinessName : SALES Source 13
    dataProductTier : sourceAligned
    }
    class sales_src_14{
    <<data-product>>
    dataProductBusinessName : SALES Source 14
    dataProductTier : sourceAligned
    }
    class sales_src_15{
    <<data-product>>
    dataProductBusinessName : SALES Source 15
    dataProductTier : sourceAligned
    }
    class sales_src_16{
    <<data-product>>
    dataProductBusinessName : SALES Source 16
    dataProductTier : sourceAligned
    }
    class sales_src_17{
    <<data-product>>
    dataProductBusinessName : SALES Source 17
    dataProductTier : sourceAligned
    }
    class sales_src_18{
    <<data-product>>
    dataProductBusinessName : SALES Source 18
    dataProductTier : sourceAligned
    }
    class sales_src_19{
    <<data-product>>
    dataProductBusinessName : SALES Source 19
    dataProductTier : sourceAligned
    }
    class sales_src_20{
    <<data-product>>
    dataProductBusinessName : SALES Source 20
    dataProductTier : sourceAligned
    }
    class sales_src_21{
    <<data-product>>
    dataProductBusinessName : SALES Source 21
    dataProductTier : sourceAligned
    }
    class sales_src_22{
    <<data-product>>
    dataProductBusinessName : SALES Source 22
    dataProductTier : sourceAligned
    }
    class sales_src_23{
    <<data-product>>
    dataProductBusinessName : SALES Source 23
    dataProductTier : sourceAligned
    }
    class sales_src_24{
    <<data-product>>
    dataProductBusinessName : SALES Source 24
    dataProductTier : sourceAligned
    }
    class sales_src_25{
    <<data-product>>
    dataProductBusinessName : SALES Source 25
    dataProductTier : sourceAligned
    }
    class sales_src_26{
    <<data-product>>
    dataProductBusinessName : SALES Source 26
    dataProductTier : sourceAligned
    }
    class sales_src_27{
    <<data-product>>
    dataProductBusinessName : SALES Source 27
    dataProductTier : sourceAligned
    }
    class sales_src_28{
    <<data-product>>
    dataProductBusinessName : SALES Source 28
    dataProductTier : sourceAligned
    }
    class sales_src_29{
    <<data-product>>
    dataProductBusinessName : SALES Source 29
    dataProductTier : sourceAligned
    }
    class sales_src_30{
    <<data-product>>
    dataProductBusinessName : SALES Source 30
    dataProductTier : sourceAligned
    }
    class sales_src_31{
    <<data-product>>
    dataProductBusinessName : SALES Source 31
    dataProductTier : sourceAligned
    }
    class sales_src_32{
    <<data-product>>
    dataProductBusinessName : SALES Source 32
    dataProductTier : sourceAligned
    }
    class sales_src_33{
    <<data-product>>
    dataProductBusinessName : SALES Source 33
    dataProductTier : sourceAligned
    }
    class sales_src_34{
    <<data-product>>
    dataProductBusinessName : SALES Source 34
    dataProductTier : sourceAligned
    }
    class sales_src_35{
    <<data-product>>
    dataProductBusinessName : SALES Source 35
    dataProductTier : sourceAligned
    }
    class sales_src_36{
    <<data-product>>
    dataProductBusinessName : SALES Source 36
    dataProductTier : sourceAligned
    }
    class sales_src_37{
    <<data-product>>
    dataProductBusinessName : SALES Source 37
    dataProductTier : sourceAligned
    }
    class sales_src_38{
    <<data-product>>
    dataProductBusinessName : SALES Source 38
    dataProductTier : sourceAligned
    }
    class sales_src_39{
    <<data-product>>
    dataProductBusinessName : SALES Source 39
    dataProductTier : sourceAligned
    }
    class sales_src_40{
    <<data-product>>
    dataProductBusinessName : SALES Source 40
    dataProductTier : sourceAligned
    }
    class sales_src_41{
    <<data-product>>
    dataProductBusinessName : SALES Source 41
    dataProductTier : sourceAligned
    }
    class sales_src_42{
    <<data-product>>
    dataProductBusinessName : SALES Source 42
    dataProductTier : sourceAligned
    }
    class sales_src_43{
    <<data-product>>
    dataProductBusinessName : SALES Source 43
    dataProductTier : sourceAligned
    }
    class sales_src_44{
    <<data-product>>
    dataProductBusinessName : SALES Source 44
    dataProductTier : sourceAligned
    }
    class sales_src_45{
    <<data-product>>
    dataProductBusinessName : SALES Source 45
    dataProductTier : sourceAligned
    }
    class sales_src_46{
    <<data-product>>
    dataProductBusinessName : SALES Source 46
    dataProductTier : sourceAligned
    }
    class sales_src_47{
    <<data-product>>
    dataProductBusinessName : SALES Source 47
    dataProductTier : sourceAligned
    }
    class sales_src_48{
    <<data-product>>
    dataProductBusinessName : SALES Source 48
    dataProductTier : sourceAligned
    }
    class sales_src_49{
    <<data-product>>
    dataProductBusinessName : SALES Source 49
    dataProductTier : sourceAligned
    }
    class sales_src_50{
    <<data-product>>
    dataProductBusinessName : SALES Source 50
    dataProductTier : sourceAligned
    }
    class sales_cur_1{
    <<data-product>>
    dataProductBusinessName : SALES Curated 1
    dataProductTier : curated
    }
    class sales_cur_2{
    <<data-product>>
    dataProductBusinessName : SALES Curated 2
    dataProductTier : curated
    }
    class sales_cur_3{
    <<data-product>>
    dataProductBusinessName : SALES Curated 3
    dataProductTier : curated
    }
    class sales_cur_4{
    <<data-product>>
    dataProductBusinessName : SALES Curated 4
    dataProductTier : curated
    }
    class sales_cur_5{
    <<data-product>>
    dataProductBusinessName : SALES Curated 5
    dataProductTier : curated
    }
    class sales_cur_6{
    <<data-product>>
    dataProductBusinessName : SALES Curated 6
    dataProductTier : curated
    }
    class sales_cur_7{
    <<data-product>>
    dataProductBusinessName : SALES Curated 7
    dataProductTier : curated
    }
    class sales_cur_8{
    <<data-product>>
    dataProductBusinessName : SALES Curated 8
    dataProductTier : curated
    }
    class sales_cur_9{
    <<data-product>>
    dataProductBusinessName : SALES Curated 9
    dataProductTier : curated
    }
    class sales_cur_10{
    <<data-product>>
    dataProductBusinessName : SALES Curated 10
    dataProductTier : curated
    }
    class sales_cur_11{
    <<data-product>>
    dataProductBusinessName : SALES Curated 11
    dataProductTier : curated
    }
    class sales_cur_12{
    <<data-product>>
    dataProductBusinessName : SALES Curated 12
    dataProductTier : curated
    }
    class sales_cur_13{
    <<data-product>>
    dataProductBusinessName : SALES Curated 13
    dataProductTier : curated
    }
    class sales_cur_14{
    <<data-product>>
    dataProductBusinessName : SALES Curated 14
    dataProductTier : curated
    }
    class sales_cur_15{
    <<data-product>>
    dataProductBusinessName : SALES Curated 15
    dataProductTier : curated
    }
    class sales_con_1{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 1
    dataProductTier : consumerAligned
    }
    class sales_con_2{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 2
    dataProductTier : consumerAligned
    }
    class sales_con_3{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 3
    dataProductTier : consumerAligned
    }
    class sales_con_4{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 4
    dataProductTier : consumerAligned
    }
    class sales_con_5{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 5
    dataProductTier : consumerAligned
    }
    class sales_con_6{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 6
    dataProductTier : consumerAligned
    }
    class sales_con_7{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 7
    dataProductTier : consumerAligned
    }
    class sales_con_8{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 8
    dataProductTier : consumerAligned
    }
    class sales_con_9{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 9
    dataProductTier : consumerAligned
    }
    class sales_con_10{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 10
    dataProductTier : consumerAligned
    }
    class sales_con_11{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 11
    dataProductTier : consumerAligned
    }
    class sales_con_12{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 12
    dataProductTier : consumerAligned
    }
    class sales_con_13{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 13
    dataProductTier : consumerAligned
    }
    class sales_con_14{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 14
    dataProductTier : consumerAligned
    }
    class sales_con_15{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 15
    dataProductTier : consumerAligned
    }
    class sales_con_16{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 16
    dataProductTier : consumerAligned
    }
    class sales_con_17{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 17
    dataProductTier : consumerAligned
    }
    class sales_con_18{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 18
    dataProductTier : consumerAligned
    }
    class sales_con_19{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 19
    dataProductTier : consumerAligned
    }
    class sales_con_20{
    <<data-product>>
    dataProductBusinessName : SALES Consumer 20
    dataProductTier : consumerAligned
    }
    class customer_src_1{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 1
    dataProductTier : sourceAligned
    }
    class customer_src_2{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 2
    dataProductTier : sourceAligned
    }
    class customer_src_3{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 3
    dataProductTier : sourceAligned
    }
    class customer_src_4{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 4
    dataProductTier : sourceAligned
    }
    class customer_src_5{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 5
    dataProductTier : sourceAligned
    }
    class customer_src_6{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 6
    dataProductTier : sourceAligned
    }
    class customer_src_7{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 7
    dataProductTier : sourceAligned
    }
    class customer_src_8{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 8
    dataProductTier : sourceAligned
    }
    class customer_src_9{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 9
    dataProductTier : sourceAligned
    }
    class customer_src_10{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 10
    dataProductTier : sourceAligned
    }
    class customer_src_11{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 11
    dataProductTier : sourceAligned
    }
    class customer_src_12{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 12
    dataProductTier : sourceAligned
    }
    class customer_src_13{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 13
    dataProductTier : sourceAligned
    }
    class customer_src_14{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 14
    dataProductTier : sourceAligned
    }
    class customer_src_15{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 15
    dataProductTier : sourceAligned
    }
    class customer_src_16{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 16
    dataProductTier : sourceAligned
    }
    class customer_src_17{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 17
    dataProductTier : sourceAligned
    }
    class customer_src_18{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 18
    dataProductTier : sourceAligned
    }
    class customer_src_19{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 19
    dataProductTier : sourceAligned
    }
    class customer_src_20{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 20
    dataProductTier : sourceAligned
    }
    class customer_src_21{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 21
    dataProductTier : sourceAligned
    }
    class customer_src_22{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 22
    dataProductTier : sourceAligned
    }
    class customer_src_23{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 23
    dataProductTier : sourceAligned
    }
    class customer_src_24{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 24
    dataProductTier : sourceAligned
    }
    class customer_src_25{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 25
    dataProductTier : sourceAligned
    }
    class customer_src_26{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 26
    dataProductTier : sourceAligned
    }
    class customer_src_27{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 27
    dataProductTier : sourceAligned
    }
    class customer_src_28{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 28
    dataProductTier : sourceAligned
    }
    class customer_src_29{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 29
    dataProductTier : sourceAligned
    }
    class customer_src_30{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 30
    dataProductTier : sourceAligned
    }
    class customer_src_31{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 31
    dataProductTier : sourceAligned
    }
    class customer_src_32{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 32
    dataProductTier : sourceAligned
    }
    class customer_src_33{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 33
    dataProductTier : sourceAligned
    }
    class customer_src_34{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 34
    dataProductTier : sourceAligned
    }
    class customer_src_35{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 35
    dataProductTier : sourceAligned
    }
    class customer_src_36{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 36
    dataProductTier : sourceAligned
    }
    class customer_src_37{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 37
    dataProductTier : sourceAligned
    }
    class customer_src_38{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 38
    dataProductTier : sourceAligned
    }
    class customer_src_39{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 39
    dataProductTier : sourceAligned
    }
    class customer_src_40{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 40
    dataProductTier : sourceAligned
    }
    class customer_src_41{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 41
    dataProductTier : sourceAligned
    }
    class customer_src_42{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 42
    dataProductTier : sourceAligned
    }
    class customer_src_43{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 43
    dataProductTier : sourceAligned
    }
    class customer_src_44{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 44
    dataProductTier : sourceAligned
    }
    class customer_src_45{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 45
    dataProductTier : sourceAligned
    }
    class customer_src_46{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 46
    dataProductTier : sourceAligned
    }
    class customer_src_47{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 47
    dataProductTier : sourceAligned
    }
    class customer_src_48{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 48
    dataProductTier : sourceAligned
    }
    class customer_src_49{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 49
    dataProductTier : sourceAligned
    }
    class customer_src_50{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Source 50
    dataProductTier : sourceAligned
    }
    class customer_cur_1{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 1
    dataProductTier : curated
    }
    class customer_cur_2{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 2
    dataProductTier : curated
    }
    class customer_cur_3{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 3
    dataProductTier : curated
    }
    class customer_cur_4{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 4
    dataProductTier : curated
    }
    class customer_cur_5{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 5
    dataProductTier : curated
    }
    class customer_cur_6{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 6
    dataProductTier : curated
    }
    class customer_cur_7{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 7
    dataProductTier : curated
    }
    class customer_cur_8{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 8
    dataProductTier : curated
    }
    class customer_cur_9{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 9
    dataProductTier : curated
    }
    class customer_cur_10{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 10
    dataProductTier : curated
    }
    class customer_cur_11{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 11
    dataProductTier : curated
    }
    class customer_cur_12{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 12
    dataProductTier : curated
    }
    class customer_cur_13{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 13
    dataProductTier : curated
    }
    class customer_cur_14{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 14
    dataProductTier : curated
    }
    class customer_cur_15{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Curated 15
    dataProductTier : curated
    }
    class customer_con_1{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 1
    dataProductTier : consumerAligned
    }
    class customer_con_2{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 2
    dataProductTier : consumerAligned
    }
    class customer_con_3{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 3
    dataProductTier : consumerAligned
    }
    class customer_con_4{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 4
    dataProductTier : consumerAligned
    }
    class customer_con_5{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 5
    dataProductTier : consumerAligned
    }
    class customer_con_6{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 6
    dataProductTier : consumerAligned
    }
    class customer_con_7{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 7
    dataProductTier : consumerAligned
    }
    class customer_con_8{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 8
    dataProductTier : consumerAligned
    }
    class customer_con_9{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 9
    dataProductTier : consumerAligned
    }
    class customer_con_10{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 10
    dataProductTier : consumerAligned
    }
    class customer_con_11{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 11
    dataProductTier : consumerAligned
    }
    class customer_con_12{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 12
    dataProductTier : consumerAligned
    }
    class customer_con_13{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 13
    dataProductTier : consumerAligned
    }
    class customer_con_14{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 14
    dataProductTier : consumerAligned
    }
    class customer_con_15{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 15
    dataProductTier : consumerAligned
    }
    class customer_con_16{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 16
    dataProductTier : consumerAligned
    }
    class customer_con_17{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 17
    dataProductTier : consumerAligned
    }
    class customer_con_18{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 18
    dataProductTier : consumerAligned
    }
    class customer_con_19{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 19
    dataProductTier : consumerAligned
    }
    class customer_con_20{
    <<data-product>>
    dataProductBusinessName : CUSTOMER Consumer 20
    dataProductTier : consumerAligned
    }
    %% DEPENDENCIES
```
