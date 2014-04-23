//
//  _SenderJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class SenderJSONObject;

@interface _SenderJSONObject : NSObject <NSCoding>


@property (nonatomic, strong) NSString *senderName;
@property (nonatomic, strong) NSString *previewImageURL;

+ (SenderJSONObject *)senderWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end

