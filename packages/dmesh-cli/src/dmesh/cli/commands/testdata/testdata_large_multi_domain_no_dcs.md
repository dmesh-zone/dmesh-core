```mermaid
classDiagram
    %% DOMAIN
    class inventory{
        <<domain>>
    }
    inventory --> inventory_src_1: owns
    inventory --> inventory_src_2: owns
    inventory --> inventory_src_3: owns
    inventory --> inventory_src_4: owns
    inventory --> inventory_src_5: owns
    inventory --> inventory_src_6: owns
    inventory --> inventory_src_7: owns
    inventory --> inventory_src_8: owns
    inventory --> inventory_src_9: owns
    inventory --> inventory_src_10: owns
    inventory --> inventory_src_11: owns
    inventory --> inventory_src_12: owns
    inventory --> inventory_src_13: owns
    inventory --> inventory_src_14: owns
    inventory --> inventory_src_15: owns
    inventory --> inventory_src_16: owns
    inventory --> inventory_src_17: owns
    inventory --> inventory_src_18: owns
    inventory --> inventory_src_19: owns
    inventory --> inventory_src_20: owns
    inventory --> inventory_src_21: owns
    inventory --> inventory_src_22: owns
    inventory --> inventory_src_23: owns
    inventory --> inventory_src_24: owns
    inventory --> inventory_src_25: owns
    inventory --> inventory_src_26: owns
    inventory --> inventory_src_27: owns
    inventory --> inventory_src_28: owns
    inventory --> inventory_src_29: owns
    inventory --> inventory_src_30: owns
    inventory --> inventory_src_31: owns
    inventory --> inventory_src_32: owns
    inventory --> inventory_src_33: owns
    inventory --> inventory_src_34: owns
    inventory --> inventory_src_35: owns
    inventory --> inventory_src_36: owns
    inventory --> inventory_src_37: owns
    inventory --> inventory_src_38: owns
    inventory --> inventory_src_39: owns
    inventory --> inventory_src_40: owns
    inventory --> inventory_src_41: owns
    inventory --> inventory_src_42: owns
    inventory --> inventory_src_43: owns
    inventory --> inventory_src_44: owns
    inventory --> inventory_src_45: owns
    inventory --> inventory_src_46: owns
    inventory --> inventory_src_47: owns
    inventory --> inventory_src_48: owns
    inventory --> inventory_src_49: owns
    inventory --> inventory_src_50: owns
    inventory --> inventory_cur_1: owns
    inventory --> inventory_cur_2: owns
    inventory --> inventory_cur_3: owns
    inventory --> inventory_cur_4: owns
    inventory --> inventory_cur_5: owns
    inventory --> inventory_cur_6: owns
    inventory --> inventory_cur_7: owns
    inventory --> inventory_cur_8: owns
    inventory --> inventory_cur_9: owns
    inventory --> inventory_cur_10: owns
    inventory --> inventory_cur_11: owns
    inventory --> inventory_cur_12: owns
    inventory --> inventory_cur_13: owns
    inventory --> inventory_cur_14: owns
    inventory --> inventory_cur_15: owns
    inventory --> inventory_con_1: owns
    inventory --> inventory_con_2: owns
    inventory --> inventory_con_3: owns
    inventory --> inventory_con_4: owns
    inventory --> inventory_con_5: owns
    inventory --> inventory_con_6: owns
    inventory --> inventory_con_7: owns
    inventory --> inventory_con_8: owns
    inventory --> inventory_con_9: owns
    inventory --> inventory_con_10: owns
    inventory --> inventory_con_11: owns
    inventory --> inventory_con_12: owns
    inventory --> inventory_con_13: owns
    inventory --> inventory_con_14: owns
    inventory --> inventory_con_15: owns
    inventory --> inventory_con_16: owns
    inventory --> inventory_con_17: owns
    inventory --> inventory_con_18: owns
    inventory --> inventory_con_19: owns
    inventory --> inventory_con_20: owns
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
    %% CURATED DATA PRODUCT
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
    %% CONSUMER ALIGNED DATA PRODUCT
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
    %% PROVIDES RELATIONS
    inventory_src_1 --> inventory_cur_1 : provides
    inventory_src_2 --> inventory_cur_2 : provides
    inventory_src_3 --> inventory_cur_3 : provides
    inventory_src_4 --> inventory_cur_4 : provides
    inventory_src_5 --> inventory_cur_5 : provides
    inventory_src_6 --> inventory_cur_6 : provides
    inventory_src_7 --> inventory_cur_7 : provides
    inventory_src_8 --> inventory_cur_8 : provides
    inventory_src_9 --> inventory_cur_9 : provides
    inventory_src_10 --> inventory_cur_10 : provides
    inventory_src_11 --> inventory_cur_11 : provides
    inventory_src_12 --> inventory_cur_12 : provides
    inventory_src_13 --> inventory_cur_13 : provides
    inventory_src_14 --> inventory_cur_14 : provides
    inventory_src_15 --> inventory_cur_15 : provides
    inventory_src_16 --> inventory_cur_1 : provides
    inventory_src_17 --> inventory_cur_2 : provides
    inventory_src_18 --> inventory_cur_3 : provides
    inventory_src_19 --> inventory_cur_4 : provides
    inventory_src_20 --> inventory_cur_5 : provides
    inventory_src_21 --> inventory_cur_6 : provides
    inventory_src_22 --> inventory_cur_7 : provides
    inventory_src_23 --> inventory_cur_8 : provides
    inventory_src_24 --> inventory_cur_9 : provides
    inventory_src_25 --> inventory_cur_10 : provides
    inventory_src_26 --> inventory_cur_11 : provides
    inventory_src_27 --> inventory_cur_12 : provides
    inventory_src_28 --> inventory_cur_13 : provides
    inventory_src_29 --> inventory_cur_14 : provides
    inventory_src_30 --> inventory_cur_15 : provides
    inventory_src_31 --> inventory_cur_1 : provides
    inventory_src_32 --> inventory_cur_2 : provides
    inventory_src_33 --> inventory_cur_3 : provides
    inventory_src_34 --> inventory_cur_4 : provides
    inventory_src_35 --> inventory_cur_5 : provides
    inventory_src_36 --> inventory_cur_6 : provides
    inventory_src_37 --> inventory_cur_7 : provides
    inventory_src_38 --> inventory_cur_8 : provides
    inventory_src_39 --> inventory_cur_9 : provides
    inventory_src_40 --> inventory_cur_10 : provides
    inventory_src_41 --> inventory_cur_11 : provides
    inventory_src_42 --> inventory_cur_12 : provides
    inventory_src_43 --> inventory_cur_13 : provides
    inventory_src_44 --> inventory_cur_14 : provides
    inventory_src_45 --> inventory_cur_15 : provides
    inventory_src_46 --> inventory_cur_1 : provides
    inventory_src_47 --> inventory_cur_2 : provides
    inventory_src_48 --> inventory_cur_3 : provides
    inventory_src_49 --> inventory_cur_4 : provides
    inventory_src_50 --> inventory_cur_5 : provides
    inventory_cur_1 --> inventory_con_1 : provides
    inventory_cur_2 --> inventory_con_2 : provides
    inventory_cur_3 --> inventory_con_3 : provides
    inventory_cur_4 --> inventory_con_4 : provides
    inventory_cur_5 --> inventory_con_5 : provides
    inventory_cur_6 --> inventory_con_6 : provides
    inventory_cur_7 --> inventory_con_7 : provides
    inventory_cur_8 --> inventory_con_8 : provides
    inventory_cur_9 --> inventory_con_9 : provides
    inventory_cur_10 --> inventory_con_10 : provides
    inventory_cur_11 --> inventory_con_11 : provides
    inventory_cur_12 --> inventory_con_12 : provides
    inventory_cur_13 --> inventory_con_13 : provides
    inventory_cur_14 --> inventory_con_14 : provides
    inventory_cur_15 --> inventory_con_15 : provides
    inventory_cur_1 --> inventory_con_16 : provides
    inventory_cur_2 --> inventory_con_17 : provides
    inventory_cur_3 --> inventory_con_18 : provides
    inventory_cur_4 --> inventory_con_19 : provides
    inventory_cur_5 --> inventory_con_20 : provides
    %% DOMAIN
    class sales{
        <<domain>>
    }
    sales --> sales_src_1: owns
    sales --> sales_src_2: owns
    sales --> sales_src_3: owns
    sales --> sales_src_4: owns
    sales --> sales_src_5: owns
    sales --> sales_src_6: owns
    sales --> sales_src_7: owns
    sales --> sales_src_8: owns
    sales --> sales_src_9: owns
    sales --> sales_src_10: owns
    sales --> sales_src_11: owns
    sales --> sales_src_12: owns
    sales --> sales_src_13: owns
    sales --> sales_src_14: owns
    sales --> sales_src_15: owns
    sales --> sales_src_16: owns
    sales --> sales_src_17: owns
    sales --> sales_src_18: owns
    sales --> sales_src_19: owns
    sales --> sales_src_20: owns
    sales --> sales_src_21: owns
    sales --> sales_src_22: owns
    sales --> sales_src_23: owns
    sales --> sales_src_24: owns
    sales --> sales_src_25: owns
    sales --> sales_src_26: owns
    sales --> sales_src_27: owns
    sales --> sales_src_28: owns
    sales --> sales_src_29: owns
    sales --> sales_src_30: owns
    sales --> sales_src_31: owns
    sales --> sales_src_32: owns
    sales --> sales_src_33: owns
    sales --> sales_src_34: owns
    sales --> sales_src_35: owns
    sales --> sales_src_36: owns
    sales --> sales_src_37: owns
    sales --> sales_src_38: owns
    sales --> sales_src_39: owns
    sales --> sales_src_40: owns
    sales --> sales_src_41: owns
    sales --> sales_src_42: owns
    sales --> sales_src_43: owns
    sales --> sales_src_44: owns
    sales --> sales_src_45: owns
    sales --> sales_src_46: owns
    sales --> sales_src_47: owns
    sales --> sales_src_48: owns
    sales --> sales_src_49: owns
    sales --> sales_src_50: owns
    sales --> sales_cur_1: owns
    sales --> sales_cur_2: owns
    sales --> sales_cur_3: owns
    sales --> sales_cur_4: owns
    sales --> sales_cur_5: owns
    sales --> sales_cur_6: owns
    sales --> sales_cur_7: owns
    sales --> sales_cur_8: owns
    sales --> sales_cur_9: owns
    sales --> sales_cur_10: owns
    sales --> sales_cur_11: owns
    sales --> sales_cur_12: owns
    sales --> sales_cur_13: owns
    sales --> sales_cur_14: owns
    sales --> sales_cur_15: owns
    sales --> sales_con_1: owns
    sales --> sales_con_2: owns
    sales --> sales_con_3: owns
    sales --> sales_con_4: owns
    sales --> sales_con_5: owns
    sales --> sales_con_6: owns
    sales --> sales_con_7: owns
    sales --> sales_con_8: owns
    sales --> sales_con_9: owns
    sales --> sales_con_10: owns
    sales --> sales_con_11: owns
    sales --> sales_con_12: owns
    sales --> sales_con_13: owns
    sales --> sales_con_14: owns
    sales --> sales_con_15: owns
    sales --> sales_con_16: owns
    sales --> sales_con_17: owns
    sales --> sales_con_18: owns
    sales --> sales_con_19: owns
    sales --> sales_con_20: owns
    %% SOURCE ALIGNED DATA PRODUCT
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
    %% CURATED DATA PRODUCT
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
    %% CONSUMER ALIGNED DATA PRODUCT
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
    %% PROVIDES RELATIONS
    sales_src_1 --> sales_cur_1 : provides
    sales_src_2 --> sales_cur_2 : provides
    sales_src_3 --> sales_cur_3 : provides
    sales_src_4 --> sales_cur_4 : provides
    sales_src_5 --> sales_cur_5 : provides
    sales_src_6 --> sales_cur_6 : provides
    sales_src_7 --> sales_cur_7 : provides
    sales_src_8 --> sales_cur_8 : provides
    sales_src_9 --> sales_cur_9 : provides
    sales_src_10 --> sales_cur_10 : provides
    sales_src_11 --> sales_cur_11 : provides
    sales_src_12 --> sales_cur_12 : provides
    sales_src_13 --> sales_cur_13 : provides
    sales_src_14 --> sales_cur_14 : provides
    sales_src_15 --> sales_cur_15 : provides
    sales_src_16 --> sales_cur_1 : provides
    sales_src_17 --> sales_cur_2 : provides
    sales_src_18 --> sales_cur_3 : provides
    sales_src_19 --> sales_cur_4 : provides
    sales_src_20 --> sales_cur_5 : provides
    sales_src_21 --> sales_cur_6 : provides
    sales_src_22 --> sales_cur_7 : provides
    sales_src_23 --> sales_cur_8 : provides
    sales_src_24 --> sales_cur_9 : provides
    sales_src_25 --> sales_cur_10 : provides
    sales_src_26 --> sales_cur_11 : provides
    sales_src_27 --> sales_cur_12 : provides
    sales_src_28 --> sales_cur_13 : provides
    sales_src_29 --> sales_cur_14 : provides
    sales_src_30 --> sales_cur_15 : provides
    sales_src_31 --> sales_cur_1 : provides
    sales_src_32 --> sales_cur_2 : provides
    sales_src_33 --> sales_cur_3 : provides
    sales_src_34 --> sales_cur_4 : provides
    sales_src_35 --> sales_cur_5 : provides
    sales_src_36 --> sales_cur_6 : provides
    sales_src_37 --> sales_cur_7 : provides
    sales_src_38 --> sales_cur_8 : provides
    sales_src_39 --> sales_cur_9 : provides
    sales_src_40 --> sales_cur_10 : provides
    sales_src_41 --> sales_cur_11 : provides
    sales_src_42 --> sales_cur_12 : provides
    sales_src_43 --> sales_cur_13 : provides
    sales_src_44 --> sales_cur_14 : provides
    sales_src_45 --> sales_cur_15 : provides
    sales_src_46 --> sales_cur_1 : provides
    sales_src_47 --> sales_cur_2 : provides
    sales_src_48 --> sales_cur_3 : provides
    sales_src_49 --> sales_cur_4 : provides
    sales_src_50 --> sales_cur_5 : provides
    sales_cur_1 --> sales_con_1 : provides
    sales_cur_2 --> sales_con_2 : provides
    sales_cur_3 --> sales_con_3 : provides
    sales_cur_4 --> sales_con_4 : provides
    sales_cur_5 --> sales_con_5 : provides
    sales_cur_6 --> sales_con_6 : provides
    sales_cur_7 --> sales_con_7 : provides
    sales_cur_8 --> sales_con_8 : provides
    sales_cur_9 --> sales_con_9 : provides
    sales_cur_10 --> sales_con_10 : provides
    sales_cur_11 --> sales_con_11 : provides
    sales_cur_12 --> sales_con_12 : provides
    sales_cur_13 --> sales_con_13 : provides
    sales_cur_14 --> sales_con_14 : provides
    sales_cur_15 --> sales_con_15 : provides
    sales_cur_1 --> sales_con_16 : provides
    sales_cur_2 --> sales_con_17 : provides
    sales_cur_3 --> sales_con_18 : provides
    sales_cur_4 --> sales_con_19 : provides
    sales_cur_5 --> sales_con_20 : provides
    %% DOMAIN
    class customer{
        <<domain>>
    }
    customer --> customer_src_1: owns
    customer --> customer_src_2: owns
    customer --> customer_src_3: owns
    customer --> customer_src_4: owns
    customer --> customer_src_5: owns
    customer --> customer_src_6: owns
    customer --> customer_src_7: owns
    customer --> customer_src_8: owns
    customer --> customer_src_9: owns
    customer --> customer_src_10: owns
    customer --> customer_src_11: owns
    customer --> customer_src_12: owns
    customer --> customer_src_13: owns
    customer --> customer_src_14: owns
    customer --> customer_src_15: owns
    customer --> customer_src_16: owns
    customer --> customer_src_17: owns
    customer --> customer_src_18: owns
    customer --> customer_src_19: owns
    customer --> customer_src_20: owns
    customer --> customer_src_21: owns
    customer --> customer_src_22: owns
    customer --> customer_src_23: owns
    customer --> customer_src_24: owns
    customer --> customer_src_25: owns
    customer --> customer_src_26: owns
    customer --> customer_src_27: owns
    customer --> customer_src_28: owns
    customer --> customer_src_29: owns
    customer --> customer_src_30: owns
    customer --> customer_src_31: owns
    customer --> customer_src_32: owns
    customer --> customer_src_33: owns
    customer --> customer_src_34: owns
    customer --> customer_src_35: owns
    customer --> customer_src_36: owns
    customer --> customer_src_37: owns
    customer --> customer_src_38: owns
    customer --> customer_src_39: owns
    customer --> customer_src_40: owns
    customer --> customer_src_41: owns
    customer --> customer_src_42: owns
    customer --> customer_src_43: owns
    customer --> customer_src_44: owns
    customer --> customer_src_45: owns
    customer --> customer_src_46: owns
    customer --> customer_src_47: owns
    customer --> customer_src_48: owns
    customer --> customer_src_49: owns
    customer --> customer_src_50: owns
    customer --> customer_cur_1: owns
    customer --> customer_cur_2: owns
    customer --> customer_cur_3: owns
    customer --> customer_cur_4: owns
    customer --> customer_cur_5: owns
    customer --> customer_cur_6: owns
    customer --> customer_cur_7: owns
    customer --> customer_cur_8: owns
    customer --> customer_cur_9: owns
    customer --> customer_cur_10: owns
    customer --> customer_cur_11: owns
    customer --> customer_cur_12: owns
    customer --> customer_cur_13: owns
    customer --> customer_cur_14: owns
    customer --> customer_cur_15: owns
    customer --> customer_con_1: owns
    customer --> customer_con_2: owns
    customer --> customer_con_3: owns
    customer --> customer_con_4: owns
    customer --> customer_con_5: owns
    customer --> customer_con_6: owns
    customer --> customer_con_7: owns
    customer --> customer_con_8: owns
    customer --> customer_con_9: owns
    customer --> customer_con_10: owns
    customer --> customer_con_11: owns
    customer --> customer_con_12: owns
    customer --> customer_con_13: owns
    customer --> customer_con_14: owns
    customer --> customer_con_15: owns
    customer --> customer_con_16: owns
    customer --> customer_con_17: owns
    customer --> customer_con_18: owns
    customer --> customer_con_19: owns
    customer --> customer_con_20: owns
    %% SOURCE ALIGNED DATA PRODUCT
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
    %% CURATED DATA PRODUCT
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
    %% CONSUMER ALIGNED DATA PRODUCT
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
    %% PROVIDES RELATIONS
    customer_src_1 --> customer_cur_1 : provides
    customer_src_2 --> customer_cur_2 : provides
    customer_src_3 --> customer_cur_3 : provides
    customer_src_4 --> customer_cur_4 : provides
    customer_src_5 --> customer_cur_5 : provides
    customer_src_6 --> customer_cur_6 : provides
    customer_src_7 --> customer_cur_7 : provides
    customer_src_8 --> customer_cur_8 : provides
    customer_src_9 --> customer_cur_9 : provides
    customer_src_10 --> customer_cur_10 : provides
    customer_src_11 --> customer_cur_11 : provides
    customer_src_12 --> customer_cur_12 : provides
    customer_src_13 --> customer_cur_13 : provides
    customer_src_14 --> customer_cur_14 : provides
    customer_src_15 --> customer_cur_15 : provides
    customer_src_16 --> customer_cur_1 : provides
    customer_src_17 --> customer_cur_2 : provides
    customer_src_18 --> customer_cur_3 : provides
    customer_src_19 --> customer_cur_4 : provides
    customer_src_20 --> customer_cur_5 : provides
    customer_src_21 --> customer_cur_6 : provides
    customer_src_22 --> customer_cur_7 : provides
    customer_src_23 --> customer_cur_8 : provides
    customer_src_24 --> customer_cur_9 : provides
    customer_src_25 --> customer_cur_10 : provides
    customer_src_26 --> customer_cur_11 : provides
    customer_src_27 --> customer_cur_12 : provides
    customer_src_28 --> customer_cur_13 : provides
    customer_src_29 --> customer_cur_14 : provides
    customer_src_30 --> customer_cur_15 : provides
    customer_src_31 --> customer_cur_1 : provides
    customer_src_32 --> customer_cur_2 : provides
    customer_src_33 --> customer_cur_3 : provides
    customer_src_34 --> customer_cur_4 : provides
    customer_src_35 --> customer_cur_5 : provides
    customer_src_36 --> customer_cur_6 : provides
    customer_src_37 --> customer_cur_7 : provides
    customer_src_38 --> customer_cur_8 : provides
    customer_src_39 --> customer_cur_9 : provides
    customer_src_40 --> customer_cur_10 : provides
    customer_src_41 --> customer_cur_11 : provides
    customer_src_42 --> customer_cur_12 : provides
    customer_src_43 --> customer_cur_13 : provides
    customer_src_44 --> customer_cur_14 : provides
    customer_src_45 --> customer_cur_15 : provides
    customer_src_46 --> customer_cur_1 : provides
    customer_src_47 --> customer_cur_2 : provides
    customer_src_48 --> customer_cur_3 : provides
    customer_src_49 --> customer_cur_4 : provides
    customer_src_50 --> customer_cur_5 : provides
    customer_cur_1 --> customer_con_1 : provides
    customer_cur_2 --> customer_con_2 : provides
    customer_cur_3 --> customer_con_3 : provides
    customer_cur_4 --> customer_con_4 : provides
    customer_cur_5 --> customer_con_5 : provides
    customer_cur_6 --> customer_con_6 : provides
    customer_cur_7 --> customer_con_7 : provides
    customer_cur_8 --> customer_con_8 : provides
    customer_cur_9 --> customer_con_9 : provides
    customer_cur_10 --> customer_con_10 : provides
    customer_cur_11 --> customer_con_11 : provides
    customer_cur_12 --> customer_con_12 : provides
    customer_cur_13 --> customer_con_13 : provides
    customer_cur_14 --> customer_con_14 : provides
    customer_cur_15 --> customer_con_15 : provides
    customer_cur_1 --> customer_con_16 : provides
    customer_cur_2 --> customer_con_17 : provides
    customer_cur_3 --> customer_con_18 : provides
    customer_cur_4 --> customer_con_19 : provides
    customer_cur_5 --> customer_con_20 : provides
```
