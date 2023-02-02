/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 * From ASN.1 module "E2SM-HelloWorld-IEs"
 * 	found in "e2sm-HelloWorld-v001.asn"
 * 	`asn1c -fno-include-deps -fcompound-names -findirect-choice -gen-PER -no-gen-OER`
 */

#include "E2SM-HelloWorld-ActionDefinition.h"

#include "E2SM-HelloWorld-ActionDefinition-Format1.h"
static asn_per_constraints_t asn_PER_type_E2SM_HelloWorld_ActionDefinition_constr_1 CC_NOTUSED = {
	{ APC_CONSTRAINED | APC_EXTENSIBLE,  0,  0,  0,  0 }	/* (0..0,...) */,
	{ APC_UNCONSTRAINED,	-1, -1,  0,  0 },
	0, 0	/* No PER value map */
};
static asn_TYPE_member_t asn_MBR_E2SM_HelloWorld_ActionDefinition_1[] = {
	{ ATF_POINTER, 0, offsetof(struct E2SM_HelloWorld_ActionDefinition, choice.actionDefinition_Format1),
		(ASN_TAG_CLASS_CONTEXT | (0 << 2)),
		-1,	/* IMPLICIT tag at current level */
		&asn_DEF_E2SM_HelloWorld_ActionDefinition_Format1,
		0,
		{ 0, 0, 0 },
		0, 0, /* No default value */
		"actionDefinition-Format1"
		},
};
static const asn_TYPE_tag2member_t asn_MAP_E2SM_HelloWorld_ActionDefinition_tag2el_1[] = {
    { (ASN_TAG_CLASS_CONTEXT | (0 << 2)), 0, 0, 0 } /* actionDefinition-Format1 */
};
static asn_CHOICE_specifics_t asn_SPC_E2SM_HelloWorld_ActionDefinition_specs_1 = {
	sizeof(struct E2SM_HelloWorld_ActionDefinition),
	offsetof(struct E2SM_HelloWorld_ActionDefinition, _asn_ctx),
	offsetof(struct E2SM_HelloWorld_ActionDefinition, present),
	sizeof(((struct E2SM_HelloWorld_ActionDefinition *)0)->present),
	asn_MAP_E2SM_HelloWorld_ActionDefinition_tag2el_1,
	1,	/* Count of tags in the map */
	0, 0,
	1	/* Extensions start */
};
asn_TYPE_descriptor_t asn_DEF_E2SM_HelloWorld_ActionDefinition = {
	"E2SM-HelloWorld-ActionDefinition",
	"E2SM-HelloWorld-ActionDefinition",
	&asn_OP_CHOICE,
	0,	/* No effective tags (pointer) */
	0,	/* No effective tags (count) */
	0,	/* No tags (pointer) */
	0,	/* No tags (count) */
	{ 0, &asn_PER_type_E2SM_HelloWorld_ActionDefinition_constr_1, CHOICE_constraint },
	asn_MBR_E2SM_HelloWorld_ActionDefinition_1,
	1,	/* Elements count */
	&asn_SPC_E2SM_HelloWorld_ActionDefinition_specs_1	/* Additional specs */
};

